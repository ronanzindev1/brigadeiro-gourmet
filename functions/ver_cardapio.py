from __main__ import app
from database.db import buscar_cardapio
from flask import Response
import json

@app.route('/cardapio', methods=['GET'])
def ver_cardapio():
    try:
        cardapio = buscar_cardapio()
        return Response(json.dumps(cardapio), status=200, headers={"Content-Type": "application/json"})
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, headers={"Content-Type": "application/json"})