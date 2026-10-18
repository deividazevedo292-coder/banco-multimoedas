# 🏦 Banco Multimoedas

Sistema bancário simples feito em Python, rodando no terminal. O usuário faz login, deposita reais e converte para dólar, euro ou libra, consulta os saldos e faz saques.

> Projeto didático, feito para praticar lógica de programação em Python.

## Funcionalidades

- **Login com usuário e senha**: a senha fica oculta enquanto é digitada, e o acesso é bloqueado após 3 tentativas erradas
- **Contas separadas**: cada usuário tem os próprios saldos
- **Depósito com conversão**: deposita em reais e converte para Dólar, Euro ou Libra
- **Consulta de saldos** em todas as moedas
- **Saque** com verificação de saldo suficiente
- **Validação de entradas**: aceita valores com vírgula (`10,50`) e não quebra com texto inválido
- **Troca de usuário**: ao sair da conta, volta para a tela de login

## Como rodar

Precisa ter o [Python 3](https://www.python.org/downloads/) instalado.

```bash
git clone https://github.com/SEU-USUARIO/banco-multimoedas.git
cd banco-multimoedas
python3 conversor.py
```

> Rode pelo terminal. A senha oculta (`getpass`) pode não funcionar no console de depuração de algumas IDEs.

## Usuários de teste

| Usuário   | Senha      |
|-----------|------------|
| `cliente` | `1234`     |
| `admin`   | `senha123` |

## Cotações usadas

As cotações são fixas no código (valor de 1 unidade em reais):

| Moeda | Cotação |
|-------|---------|
| Dólar | R$ 5,00 |
| Euro  | R$ 5,67 |
| Libra | R$ 6,67 |

## Próximos passos

- [ ] Cadastro de novos usuários
- [ ] Extrato com histórico de operações
- [ ] Salvar os dados em arquivo (JSON)
- [ ] Buscar cotações reais pela internet
- [ ] Guardar as senhas com hash

## Tecnologias

- Python 3
