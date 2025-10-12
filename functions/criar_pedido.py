from __main__ import app
from flask import request, Response
from database.db import salvar_pedido, verifica_estoque
import json
from sqs.fila import salva_pedido_fila
@app.route('/pedido', methods=['POST'])
def criar_pedido():
    try:
        payload = request.get_json()
        estoque = verifica_estoque(payload["sabor"])
        pedido = salvar_pedido(payload)
        if estoque is None:
            return Response(json.dumps({"error": "Sabor não encontrado"}), status=404, headers={"Content-Type": "application/json"})
        salva_pedido_fila(pedido)
        return Response(json.dumps(pedido), status=201, headers={"Content-Type": "application/json"})
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, headers={"Content-Type": "application/json"})
