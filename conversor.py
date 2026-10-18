#banco multimoedas


import sys
from getpass import getpass

# ===== COTAÇÕES (valor de 1 unidade em reais) =====
MOEDAS = {
    "1": {"nome": "Dólar", "simbolo": "US$", "cotacao": 5.00},
    "2": {"nome": "Euro", "simbolo": "€", "cotacao": 5.67},
    "3": {"nome": "Libra", "simbolo": "£", "cotacao": 6.67},
}

TENTATIVAS_MAXIMAS = 3


def criar_conta(senha):
    """Cria uma conta nova com todos os saldos zerados."""
    return {
        "senha": senha,
        "total_reais": 0.0,
        "saldos": {codigo: 0.0 for codigo in MOEDAS},
    }


# ===== USUÁRIOS CADASTRADOS =====
# cada usuário tem a própria senha e os próprios saldos
USUARIOS = {
    "cliente": criar_conta("1234"),
    "admin": criar_conta("senha123"),
}


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


def escolher_moeda(conta=None):
    """Mostra as moedas (com saldo, se a conta for informada) e retorna o código escolhido."""
    for codigo, moeda in MOEDAS.items():
        linha = f"{codigo} - {moeda['nome']}"
        if conta is not None:
            linha += f"  (saldo: {moeda['simbolo']} {conta['saldos'][codigo]:.2f})"
        print(linha)

    codigo = input("Moeda: ")
    if codigo not in MOEDAS:
        print("Moeda inválida.")
        return None
    return codigo


def fazer_login():
    print("\n===== LOGIN - BANCO MULTIMOEDAS =====")
    print("(digite 'sair' no usuário para fechar o programa)")

    for tentativa in range(1, TENTATIVAS_MAXIMAS + 1):
        usuario = input("Usuário: ").strip().lower()

        if usuario == "sair":
            return None

        senha = getpass("Senha: ")  # a senha não aparece enquanto digita

        if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
            print(f"\nLogin realizado! Bem-vindo, {usuario}.")
            return usuario

        restantes = TENTATIVAS_MAXIMAS - tentativa
        if restantes > 0:
            print(f"Usuário ou senha incorretos. Restam {restantes} tentativa(s).\n")

    print("Número máximo de tentativas atingido. Acesso bloqueado.")
    sys.exit()


def depositar(conta):
    deposito = ler_valor("Valor do depósito em reais: R$ ")
    if deposito is None:
        return

    print("\nEscolha a moeda:")
    codigo = escolher_moeda()
    if codigo is None:
        return

    moeda = MOEDAS[codigo]
    convertido = deposito / moeda["cotacao"]
    conta["saldos"][codigo] += convertido
    conta["total_reais"] += deposito

    print(f"Você recebeu {moeda['simbolo']} {convertido:.2f}")
    print("Depósito realizado com sucesso!")


def consultar(conta):
    print(f"Total depositado em reais: R$ {conta['total_reais']:.2f}")
    for codigo, moeda in MOEDAS.items():
        print(f"Saldo em {moeda['nome'].lower()}: {moeda['simbolo']} {conta['saldos'][codigo]:.2f}")


def sacar(conta):
    print("\nDe qual moeda deseja sacar?")
    codigo = escolher_moeda(conta)
    if codigo is None:
        return

    saque = ler_valor("Valor do saque: ")
    if saque is None:
        return

    moeda = MOEDAS[codigo]
    saldo = conta["saldos"][codigo]

    if saque > saldo:
        print(f"Saldo insuficiente. Você tem {moeda['simbolo']} {saldo:.2f}")
        return

    conta["saldos"][codigo] -= saque
    print(f"Saque de {moeda['simbolo']} {saque:.2f} realizado! "
          f"Saldo restante: {moeda['simbolo']} {conta['saldos'][codigo]:.2f}")


def menu(usuario):
    conta = USUARIOS[usuario]

    while True:
        print("\n===== BANCO MULTIMOEDAS =====")
        print(f"Usuário: {usuario}")
        print("1 - Depositar e converter")
        print("2 - Consultar saldos")
        print("3 - Sacar")
        print("0 - Sair da conta")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            depositar(conta)
        elif opcao == "2":
            consultar(conta)
        elif opcao == "3":
            sacar(conta)
        elif opcao == "0":
            print(f"Até logo, {usuario}!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# ===== INÍCIO DO PROGRAMA =====
while True:
    usuario_logado = fazer_login()
    if usuario_logado is None:
        print("Obrigado por usar o Banco Multimoedas!")
        break
    menu(usuario_logado)
