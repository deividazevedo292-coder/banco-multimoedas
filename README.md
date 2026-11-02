# 🏦 Banco Multimoedas

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20evolução-yellow)
![Interface](https://img.shields.io/badge/interface-terminal-black)

Sistema bancário feito em Python que roda no terminal. O usuário faz login, deposita em reais, converte para **dólar, euro ou libra**, consulta os saldos e faz saques — cada conta com os próprios saldos.

> Projeto de estudo criado para praticar lógica de programação, organização do código em funções e validação de entradas do usuário.

---

## 🖥️ Demonstração

```
===== LOGIN - BANCO MULTIMOEDAS =====
(digite 'sair' no usuário para fechar o programa)
Usuário: cliente
Senha:

Login realizado! Bem-vindo, cliente.

===== BANCO MULTIMOEDAS =====
Usuário: cliente
1 - Depositar e converter
2 - Consultar saldos
3 - Sacar
0 - Sair da conta
Escolha uma opção: 1
Valor do depósito em reais: R$ 100

Escolha a moeda:
1 - Dólar
2 - Euro
3 - Libra
Moeda: 1
Você recebeu US$ 20.00
Depósito realizado com sucesso!
```

---

## ✨ Funcionalidades

- **Login com usuário e senha** — a senha fica oculta enquanto é digitada e o acesso é bloqueado após 3 tentativas erradas
- **Contas separadas** — cada usuário tem os próprios saldos
- **Depósito com conversão** — deposita em reais e converte para Dólar, Euro ou Libra
- **Consulta de saldos** em todas as moedas
- **Saque** com verificação de saldo suficiente
- **Validação de entradas** — aceita valores com vírgula (`10,50`), recusa valores negativos ou zero e não quebra com texto inválido
- **Troca de usuário** — ao sair da conta, o programa volta para a tela de login

---

## 🚀 Como rodar

Precisa ter o [Python 3](https://www.python.org/downloads/) instalado. Não usa nenhuma biblioteca externa.

```bash
git clone https://github.com/deividazevedo292-coder/banco-multimoedas.git
cd banco-multimoedas
python3 conversor.py
```

> 💡 Rode pelo terminal. A senha oculta (`getpass`) pode não funcionar no console de depuração de algumas IDEs.

### Usuários de teste

| Usuário   | Senha      |
| --------- | ---------- |
| `cliente` | `1234`     |
| `admin`   | `senha123` |

---

## 🧩 Como o código está organizado

Todo o programa está em `conversor.py`, dividido em funções com uma responsabilidade cada:

| Função | O que faz |
| ------ | --------- |
| `criar_conta()` | Cria uma conta com todos os saldos zerados |
| `fazer_login()` | Pede usuário e senha, controla as 3 tentativas |
| `menu()` | Mostra as opções e chama a função escolhida |
| `depositar()` | Recebe reais e converte para a moeda escolhida |
| `consultar()` | Mostra o total depositado e os saldos |
| `sacar()` | Saca de uma moeda, verificando o saldo |
| `ler_valor()` | Lê e valida números digitados (com `try/except`) |
| `escolher_moeda()` | Lista as moedas e valida a escolha |

As moedas e os usuários ficam em **dicionários** (`MOEDAS` e `USUARIOS`), então adicionar uma moeda nova é só incluir uma linha no dicionário — o resto do código se adapta sozinho.

### Cotações usadas

As cotações são fixas no código (valor de 1 unidade em reais):

| Moeda | Cotação |
| ----- | ------- |
| Dólar | R$ 5,00 |
| Euro  | R$ 5,67 |
| Libra | R$ 6,67 |

---

## 📚 O que pratiquei

- Estruturas de repetição (`while`, `for`) e condicionais
- Funções com responsabilidade única e reaproveitamento de código
- Dicionários aninhados para guardar contas e moedas
- Tratamento de erros com `try/except`
- Entrada segura de senha com `getpass`

---

## 🛣️ Próximos passos

- [ ] Cadastro de novos usuários
- [ ] Extrato com histórico de operações
- [ ] Salvar os dados em arquivo (JSON)
- [ ] Buscar cotações reais pela internet (API do Banco Central)
- [ ] Guardar as senhas com hash

> 📊 Veja também: **[Análise de Câmbio](https://github.com/deividazevedo292-coder/analise-cambio)** — projeto complementar que analisa o histórico real das cotações com dados do Banco Central, com [dashboard online](https://dashboard-cambio-deivid.streamlit.app).

---

## 👤 Autor

**Deivid Azevedo Dantas** — estudante de Análise e Desenvolvimento de Sistemas na FMU

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/deivid-azevedo-4b5709344/)
[![Portfólio](https://img.shields.io/badge/Portfólio-000000?logo=githubpages&logoColor=white)](https://silvaxzy.github.io/)
