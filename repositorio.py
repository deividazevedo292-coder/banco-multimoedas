import hashlib
import secrets
from decimal import Decimal

from db import conectar

ITERACOES = 100_000


# ===== SENHAS =====

def hash_senha(senha):
    """Gera um hash seguro da senha (nunca guardamos a senha em si)."""
    sal = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(sal), ITERACOES)
    return f"{sal}${h.hex()}"


def verificar_senha(senha, senha_hash):
    sal, h_salvo = senha_hash.split("$")
    h = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(sal), ITERACOES)
    return secrets.compare_digest(h.hex(), h_salvo)


# ===== USUÁRIOS =====

def criar_usuario(usuario, senha):
    """Cria o usuário. Retorna o id, ou None se o nome já existir."""
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO usuarios (usuario, senha_hash) VALUES (%s, %s)
            ON CONFLICT (usuario) DO NOTHING
            RETURNING id
        """, (usuario, hash_senha(senha)))
        linha = cur.fetchone()
        return linha[0] if linha else None


def autenticar(usuario, senha):
    """Retorna o id do usuário se usuário e senha estiverem certos, senão None."""
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, senha_hash FROM usuarios WHERE usuario = %s", (usuario,))
        linha = cur.fetchone()
    if linha and verificar_senha(senha, linha[1]):
        return linha[0]
    return None


# ===== MOEDAS E SALDOS =====

def listar_moedas():
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("SELECT codigo, nome, simbolo, cotacao FROM moedas ORDER BY cotacao")
        return cur.fetchall()


def consultar_saldos(usuario_id):
    """Saldo em todas as moedas (zero se o usuário ainda não tiver nenhum)."""
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT m.codigo, m.nome, m.simbolo, COALESCE(s.valor, 0)
            FROM moedas m
            LEFT JOIN saldos s ON s.moeda = m.codigo AND s.usuario_id = %s
            ORDER BY m.cotacao
        """, (usuario_id,))
        return cur.fetchall()


def total_depositado(usuario_id):
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT COALESCE(SUM(valor_reais), 0) FROM movimentacoes
            WHERE usuario_id = %s AND tipo = 'deposito'
        """, (usuario_id,))
        return cur.fetchone()[0]


# ===== OPERAÇÕES =====

def depositar(usuario_id, moeda, valor_reais):
    """Converte reais para a moeda escolhida e guarda. Retorna o valor convertido."""
    valor_reais = Decimal(str(valor_reais))
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("SELECT cotacao FROM moedas WHERE codigo = %s", (moeda,))
        cotacao = cur.fetchone()[0]
        convertido = (valor_reais / cotacao).quantize(Decimal("0.01"))

        cur.execute("""
            INSERT INTO saldos (usuario_id, moeda, valor) VALUES (%s, %s, %s)
            ON CONFLICT (usuario_id, moeda)
            DO UPDATE SET valor = saldos.valor + EXCLUDED.valor
        """, (usuario_id, moeda, convertido))

        cur.execute("""
            INSERT INTO movimentacoes (usuario_id, tipo, moeda, valor_moeda, valor_reais, cotacao)
            VALUES (%s, 'deposito', %s, %s, %s, %s)
        """, (usuario_id, moeda, convertido, valor_reais, cotacao))
    return convertido


def sacar(usuario_id, moeda, valor):
    """Retorna True se sacou, False se o saldo não era suficiente."""
    valor = Decimal(str(valor))
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE saldos SET valor = valor - %s
            WHERE usuario_id = %s AND moeda = %s AND valor >= %s
        """, (valor, usuario_id, moeda, valor))
        if cur.rowcount == 0:
            return False

        cur.execute("""
            INSERT INTO movimentacoes (usuario_id, tipo, moeda, valor_moeda)
            VALUES (%s, 'saque', %s, %s)
        """, (usuario_id, moeda, valor))
    return True


def extrato(usuario_id):
    with conectar() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT feito_em, tipo, moeda, valor_moeda, valor_reais
            FROM movimentacoes WHERE usuario_id = %s ORDER BY feito_em
        """, (usuario_id,))
        return cur.fetchall()


# ===== TESTE RÁPIDO =====
if __name__ == "__main__":
    criar_usuario("cliente", "1234")
    criar_usuario("admin", "senha123")

    uid = autenticar("cliente", "1234")
    print("Login certo  →", uid)
    print("Senha errada →", autenticar("cliente", "0000"))
    print("Depositou R$ 100 em dólar → US$", depositar(uid, "USD", 100))
    print("Saque de US$ 5    →", sacar(uid, "USD", 5))
    print("Saque de US$ 9999 →", sacar(uid, "USD", 9999))
    for codigo, nome, simbolo, valor in consultar_saldos(uid):
        print(f"  {nome:<6} {simbolo} {valor:.2f}")
    print("Total depositado: R$", total_depositado(uid))