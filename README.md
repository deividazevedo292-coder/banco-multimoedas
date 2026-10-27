# 🏦 Banco Multimoedas

Sistema bancário feito em Python com banco de dados PostgreSQL, rodando no terminal. O usuário cria uma conta, faz login, deposita reais e converte para dólar, euro ou libra, consulta saldos, faz saques e vê o extrato. Os dados ficam salvos no banco, então nada se perde ao fechar o programa.

## Funcionalidades

- **Cadastro de usuários** direto na tela de login
- **Login seguro**: senha oculta ao digitar, armazenada com hash (PBKDF2) e bloqueio após 3 tentativas
- **Depósito com conversão** de reais para Dólar, Euro ou Libra
- **Consulta de saldos** em todas as moedas
- **Saque** com verificação de saldo feita pelo próprio banco
- **Extrato** com histórico de todas as operações
- **Dados persistentes** no PostgreSQL
- **Validação de entradas**: aceita vírgula (`10,50`) e não quebra com texto inválido

## Destaques técnicos

- **Transações**: cada operação é "tudo ou nada", então o saldo nunca fica inconsistente
- **Proteção contra SQL Injection** com consultas parametrizadas
- **`Decimal` e `NUMERIC`** para valores monetários, evitando erros de arredondamento
- **Restrições no banco** (`CHECK`, chaves estrangeiras) que impedem saldo negativo e dados inválidos
- **Separação de responsabilidades**: interface, acesso a dados e conexão em arquivos diferentes
- **Credenciais fora do código** com variáveis de ambiente (`.env`)

## Estrutura

```
banco-multimoedas/
├── conversor.py       # interface: menus e entrada do usuário
├── repositorio.py     # operações no banco de dados
├── db.py              # conexão com o PostgreSQL
├── sql/schema.sql     # criação das tabelas
├── .env.example       # modelo das variáveis de ambiente
└── requirements.txt
```

## Como rodar

Precisa ter **Python 3** e **PostgreSQL** instalados.

```bash
git clone https://github.com/deividazevedo292-coder/banco-multimoedas.git
cd banco-multimoedas

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

psql -h localhost -U postgres -c "CREATE DATABASE banco_multimoedas;"
psql -h localhost -U postgres -d banco_multimoedas -f sql/schema.sql

cp .env.example .env    # depois edite o .env com a sua senha do PostgreSQL

python conversor.py
```

Na tela de login, digite `novo` para criar uma conta.

> Rode pelo terminal. A senha oculta (`getpass`) pode não funcionar no console de depuração de algumas IDEs.

## Cotações

Ficam na tabela `moedas` (valor de 1 unidade em reais):

| Moeda | Cotação |
|-------|---------|
| Dólar | R$ 5,00 |
| Euro  | R$ 5,67 |
| Libra | R$ 6,67 |

## Próximos passos

- [x] Cadastro de novos usuários
- [x] Extrato com histórico de operações
- [x] Salvar os dados de forma persistente (PostgreSQL)
- [x] Guardar as senhas com hash
- [ ] Buscar cotações reais pela internet
- [ ] Conversão direta entre moedas estrangeiras
- [ ] Interface web

## Tecnologias

- Python 3
- PostgreSQL
- psycopg2
- python-dotenv