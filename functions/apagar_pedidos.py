from __main__ import app
from flask import Response
from database.db import limpa_tabela_pedidos
import json
@app.route('/apaga_pedidos', methods=['DELETE'])
def limpa():
    limpa_tabela_pedidos()
    return Response(json.dumps({"mensagem": "Tabela apagada com sucesso."}), status=200, mimetype="application/json")
