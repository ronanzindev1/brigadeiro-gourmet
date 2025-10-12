from __main__ import app
from flask import request, Response
from database.db import buscar_pedido
import json
@app.route('/pedido/<int:id>', methods=['GET'])
def buscar_pedido_route(id):
    try:
        pedido = buscar_pedido(id)
        if pedido is None:
            return Response(json.dumps({"error": "Pedido não encontrado"}), status=404, headers={"Content-Type": "application/json"})
        return Response(json.dumps(pedido), status=200, headers={"Content-Type": "application/json"})
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, headers={"Content-Type": "application/json"})