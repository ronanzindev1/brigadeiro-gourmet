import queue
from sns.notificacao import envia_notificacao
fila_pedidos = queue.Queue()
from database.db import atualiza_estoque, verifica_estoque, atualizar_pedido
def salva_pedido_fila(pedido):
    fila_pedidos.put(pedido)

def processar_pedido():
    while True:
        if not fila_pedidos.empty():
            mensagem = fila_pedidos.get()
            pedido = mensagem
            sabor = pedido["sabor"]
            cliente = pedido["cliente"]
            quantidade_pedido = pedido["quantidade"]
            dados_por_sabor = verifica_estoque(sabor)
            quantidade, preco_unitario = dados_por_sabor
            if quantidade < quantidade_pedido:
                atualizar_pedido(pedido["id"], "recusado", recusado_por="estoque insuficiente")
                envia_notificacao({"email": cliente, "mensagem": f"Pedido N°{pedido['id']} recusado por estoque insuficiente."})
                continue

            total = preco_unitario * quantidade_pedido
            atualizar_pedido(pedido["id"], "aceito", total=total)

            qtd_restante = quantidade - quantidade_pedido

            atualiza_estoque(sabor, qtd_restante)

            envia_notificacao({"email": cliente, "mensagem": f"Pedido N°{pedido['id']} aceito. Total: R$ {total:.2f}"})