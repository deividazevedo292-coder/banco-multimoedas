from flask import Flask, jsonify

import repositorio as repo

app = Flask(__name__)


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


@app.route("/extrato/<int:usuario_id>")
def ver_extrato(usuario_id):
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


if __name__ == "__main__":
    app.run(debug=True)