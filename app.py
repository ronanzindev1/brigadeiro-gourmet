from flask import Flask, Response
import queue
import time
from threading import Thread
from database.db import popular_banco
app = Flask(__name__)
sqs = queue.Queue()

def process_order():
    print("Order process initialized")
    while True:
        if not sqs.empty():
            order = sqs.get()
            print(order)
        else:
            time.sleep(0.5)


import functions.criar_pedido
popular_banco()
Thread(target=process_order, name="SQS", daemon=True).start()
app.run(debug=True)