from flask import Flask, Response
import queue
import time
from threading import Thread
from database.db import *
from function.envia_pedido_fila import *
from flask import request, Response
import json

app = Flask(__name__)

sqs = queue.Queue()

#apaga todos os pedidos
@app.route('/apaga_pedidos', methods=['GET'])
def limpa():
    limpa_tabela_pedidos()
    return Response(json.dumps({"mensagem": "Tabela apagada com sucesso."}), status=200, mimetype="application/json")


# primeira funcao quando chega o pedido é colocar eles na fila processar
@app.route('/enfileirar_pedidos', methods=['POST'])
def enfileirar_pedidos():
    try:       
       adicionados = envia_pedido_fila(sqs)
       return Response(json.dumps(adicionados), status=201, mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=400, mimetype="application/json")

# ver os pedidos
@app.route('/listar_pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = ver_pedidos()
    return Response(json.dumps(pedidos), status=201, mimetype="application/json")

# ver estoque
@app.route('/listar_estoque', methods=['GET'])
def listar_estoque():
    estoque = ver_estoque()
    return Response(json.dumps(estoque), status=201, mimetype="application/json")
    
def process_order():
    print("Order process initialized")
    while True:
        if not sqs.empty():
            order = sqs.get()
            print(order)
        else:
            time.sleep(0.5)
            
popular_banco()
Thread(target=process_order, name="SQS", daemon=True).start()
app.run(debug=True)