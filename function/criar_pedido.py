from __main__ import app
from flask import request, Response
from database.db import salvar_pedido
import json
@app.route('/order', methods=['POST'])
def criar_pedido():
    try:
        payload = request.get_json()
        pedido = salvar_pedido(payload)
        # sqs.put(pedido)
        return Response(json.dumps(pedido), status=201, headers={"Content-Type": "application/json"})
    except Exception as e:
        return Response(e, status=400)
