# banco multimoedas
import sys
from getpass import getpass

import repositorio as repo

TENTATIVAS_MAXIMAS = 3


def ler_valor(mensagem):
    """Lê um número digitado (aceita vírgula). Retorna None se for inválido."""
    try:
        valor = float(input(mensagem).replace(",", "."))
    except ValueError:
        print("Digite um número válido.")
        return None
    if valor <= 0:
        print("O valor deve ser maior que zero.")
        return None
    return valor


def escolher_moeda(usuario_id=None):
    """Mostra as moedas (com saldo, se informado o usuário) e retorna a escolhida."""
    if usuario_id is not None:
        linhas = repo.consultar_saldos(usuario_id)
    else:
        linhas = repo.listar_moedas()

    opcoes = {}
    for numero, linha in enumerate(linhas, start=1):
        codigo, nome, simbolo, extra = linha
        opcoes[str(numero)] = linha
        texto = f"{numero} - {nome}"
        if usuario_id is not None:
            texto += f" (saldo: {simbolo} {extra:.2f})"
        print(texto)

    escolha = input("Moeda: ")
    if escolha not in opcoes:
        print("Moeda inválida.")
        return None
    return opcoes[escolha]


def cadastrar():
    print("\n===== NOVA CONTA =====")
    usuario = input("Escolha um nome de usuário: ").strip().lower()
    if not usuario:
        print("O usuário não pode ficar vazio.")
        return
    senha = getpass("Escolha uma senha: ")
    if len(senha) < 4:
        print("A senha precisa ter pelo menos 4 caracteres.")
        return
    if getpass("Confirme a senha: ") != senha:
        print("As senhas não conferem.")
        return
    if repo.criar_usuario(usuario, senha) is None:
        print("Esse usuário já existe.")
    else:
        print(f"Conta criada! Agora é só entrar como '{usuario}'.\n")


def fazer_login():
    print("\n===== LOGIN - BANCO MULTIMOEDAS =====")
    print("(digite 'novo' para criar uma conta ou 'sair' para fechar)")
    tentativas = 0
    while tentativas < TENTATIVAS_MAXIMAS:
        usuario = input("Usuário: ").strip().lower()
        if usuario == "sair":
            return None
        if usuario == "novo":
            cadastrar()
            continue

        senha = getpass("Senha: ")  # a senha não aparece enquanto digita
        usuario_id = repo.autenticar(usuario, senha)
        if usuario_id is not None:
            print(f"\nLogin realizado! Bem-vindo, {usuario}.")
            return usuario, usuario_id

        tentativas += 1
        restantes = TENTATIVAS_MAXIMAS - tentativas
        if restantes > 0:
            print(f"Usuário ou senha incorretos. Restam {restantes} tentativa(s).\n")

    print("Número máximo de tentativas atingido. Acesso bloqueado.")
    sys.exit()


def depositar(usuario_id):
    deposito = ler_valor("Valor do depósito em reais: R$ ")
    if deposito is None:
        return
    print("\nEscolha a moeda:")
    moeda = escolher_moeda()
    if moeda is None:
        return
    codigo, nome, simbolo, cotacao = moeda
    convertido = repo.depositar(usuario_id, codigo, deposito)
    print(f"Você recebeu {simbolo} {convertido:.2f}")
    print("Depósito realizado com sucesso!")


def consultar(usuario_id):
    print(f"Total depositado em reais: R$ {repo.total_depositado(usuario_id):.2f}")
    for codigo, nome, simbolo, valor in repo.consultar_saldos(usuario_id):
        print(f"Saldo em {nome.lower()}: {simbolo} {valor:.2f}")


def sacar(usuario_id):
    print("\nDe qual moeda deseja sacar?")
    moeda = escolher_moeda(usuario_id)
    if moeda is None:
        return
    codigo, nome, simbolo, saldo = moeda
    saque = ler_valor("Valor do saque: ")
    if saque is None:
        return
    if repo.sacar(usuario_id, codigo, saque):
        print(f"Saque de {simbolo} {saque:.2f} realizado!")
    else:
        print(f"Saldo insuficiente. Você tem {simbolo} {saldo:.2f}")


def ver_extrato(usuario_id):
    movimentos = repo.extrato(usuario_id)
    if not movimentos:
        print("Nenhuma movimentação ainda.")
        return
    print("\n===== EXTRATO =====")
    for feito_em, tipo, moeda, valor_moeda, valor_reais in movimentos:
        linha = f"{feito_em:%d/%m/%Y %H:%M}  {tipo:<9} {moeda} {valor_moeda:>10.2f}"
        if valor_reais is not None:
            linha += f"  (R$ {valor_reais:.2f})"
        print(linha)


def menu(usuario, usuario_id):
    while True:
        print("\n===== BANCO MULTIMOEDAS =====")
        print(f"Usuário: {usuario}")
        print("1 - Depositar e converter")
        print("2 - Consultar saldos")
        print("3 - Sacar")
        print("4 - Extrato")
        print("0 - Sair da conta")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            depositar(usuario_id)
        elif opcao == "2":
            consultar(usuario_id)
        elif opcao == "3":
            sacar(usuario_id)
        elif opcao == "4":
            ver_extrato(usuario_id)
        elif opcao == "0":
            print(f"Até logo, {usuario}!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# ===== INÍCIO DO PROGRAMA =====
if __name__ == "__main__":
    while True:
        login = fazer_login()
        if login is None:
            print("Obrigado por usar o Banco Multimoedas!")
            break
        menu(*login)