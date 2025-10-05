from flask import Flask, request, Response
import queue
import time
import sqlite3
import uuid
import json
from threading import Thread
from database.db import popular_banco, salvar_pedido
app = Flask(__name__)
sqs = queue.Queue()
@app.route('/order', methods=['POST'])
def criar_pedido():
    try:
        payload = request.get_json()
        pedido = salvar_pedido(payload)
        sqs.put(pedido)
        return Response(json.dumps(pedido), status=201, headers={"Content-Type": "application/json"})
    except Exception as e:
        return Response(e, status=400)

def process_order():
    print("Order process initialized")
    while True:
        if not sqs.empty():
            order = sqs.get()
            print(order)
        else:
            time.sleep(0.5)


if __name__ == '__main__':
    popular_banco()
    Thread(target=process_order, name="SQS", daemon=True).start()
    app.run(debug=True)