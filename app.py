from flask import Flask
from threading import Thread
from database.db import *
from sqs.fila import processar_pedido
from sns.notificacao import processar_notificacao
app = Flask(__name__)



from functions.criar_pedido import *
from functions.buscar_pedido  import *
from functions.ver_cardapio import *
from functions.ver_pedidos import *
from functions.apagar_pedidos import *
popular_banco()
Thread(target=processar_pedido, name="SQS", daemon=True).start()
Thread(target=processar_notificacao, name="SNS", daemon=True).start()
app.run(debug=True, port=5000)