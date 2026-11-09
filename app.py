from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
from functools import wraps

import repositorio as repo

app = Flask(__name__)
app.secret_key = "banco-multimoedas-chave-secreta-123"


def login_obrigatorio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ===== LOGIN E CADASTRO =====

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]

        novo_id = repo.criar_usuario(usuario, senha)
        if novo_id is None:
            flash("Esse usuário já existe.")
            return redirect(url_for("cadastro"))

        flash("Conta criada! Faça login.")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"]

        usuario_id = repo.autenticar(usuario, senha)
        if usuario_id is None:
            flash("Usuário ou senha incorretos.")
            return redirect(url_for("login"))

        session["usuario_id"] = usuario_id
        session["nome"] = usuario
        return redirect(url_for("inicio"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ===== PÁGINAS E API =====

@app.route("/")
@login_obrigatorio
def inicio():
    return render_template("index.html")


@app.route("/moedas")
def moedas():
    linhas = repo.listar_moedas()
    resultado = []
    for codigo, nome, simbolo, cotacao in linhas:
        resultado.append({
            "codigo": codigo,
            "nome": nome,
            "simbolo": simbolo,
            "cotacao": float(cotacao),
        })
    return jsonify(resultado)


@app.route("/extrato")
@login_obrigatorio
def ver_extrato():
    usuario_id = session["usuario_id"]
    movimentos = repo.extrato(usuario_id)
    resultado = []
    for feito_em, tipo, moeda, valor_moeda, valor_reais in movimentos:
        if valor_reais is not None:
            valor_reais = float(valor_reais)
        resultado.append({
            "data": feito_em.strftime("%d/%m/%Y %H:%M"),
            "tipo": tipo,
            "moeda": moeda,
            "valor_moeda": float(valor_moeda),
            "valor_reais": valor_reais,
        })
    return jsonify(resultado)


@app.route("/saldos")
@login_obrigatorio
def ver_saldos():
    usuario_id = session["usuario_id"]
    linhas = repo.consultar_saldos(usuario_id)
    saldos = []
    for codigo, nome, simbolo, valor in linhas:
        saldos.append({
            "codigo": codigo,
            "nome": nome,
            "simbolo": simbolo,
            "valor": float(valor),
        })
    return jsonify({
        "total_depositado_reais": float(repo.total_depositado(usuario_id)),
        "saldos": saldos,
    })


def validar_pedido(dados):
    """Confere se o pedido tem uma moeda que existe e um valor maior que zero.
    Retorna uma mensagem de erro, ou None se estiver tudo certo."""
    codigos = [linha[0] for linha in repo.listar_moedas()]
    if dados.get("moeda") not in codigos:
        return "Moeda inválida."
    valor = dados.get("valor")
    if not isinstance(valor, (int, float)) or valor <= 0:
        return "O valor deve ser um número maior que zero."
    return None


@app.route("/depositar", methods=["POST"])
@login_obrigatorio
def depositar():
    usuario_id = session["usuario_id"]
    dados = request.get_json(silent=True) or {}
    erro = validar_pedido(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    convertido = repo.depositar(usuario_id, dados["moeda"], dados["valor"])
    return jsonify({
        "mensagem": "Depósito realizado com sucesso!",
        "valor_convertido": float(convertido),
    })


@app.route("/sacar", methods=["POST"])
@login_obrigatorio
def sacar():
    usuario_id = session["usuario_id"]
    dados = request.get_json(silent=True) or {}
    erro = validar_pedido(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    if repo.sacar(usuario_id, dados["moeda"], dados["valor"]):
        return jsonify({"mensagem": "Saque realizado com sucesso!"})
    return jsonify({"erro": "Saldo insuficiente."}), 400


if __name__ == "__main__":
    app.run(debug=True)