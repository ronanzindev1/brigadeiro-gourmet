from __main__ import app
import json
from flask import Response
from database.db import ver_pedidos

@app.route('/listar_pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = ver_pedidos()
    return Response(json.dumps(pedidos), status=201, mimetype="application/json")
