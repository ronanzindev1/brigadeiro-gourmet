import queue
snq = queue.Queue()
def envia_notificacao(mensagem):
    snq.put(mensagem)

def processar_notificacao():
    while True:
        if not snq.empty():
            mensagem = snq.get()
            print(f"Email {mensagem['email']}, mensagem -> ", mensagem['mensagem'])