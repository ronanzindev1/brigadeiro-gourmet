from database.db import *
from flask import request, Response
import json

def envia_pedido_fila(sqs):
    payload = request.get_json()
    adicionados = []
    for pedido in payload:
        sqs.put(pedido)
        adicionados.append(pedido)
        print(f"Queue size: {sqs.qsize()}")
    print(adicionados)    
    #aqui processa os pedidos da fila
    processar_pedido(sqs) 
    return adicionados
    
    
# ///////////////////////////  
    
    
def processar_pedido(fila_pedidos):
    print("🔁 Função consumir_fila foi chamada")
    print(f"📦 Tamanho da fila: {fila_pedidos.qsize()}")
    
    while not fila_pedidos.empty():
        print("entrou while")
        mensagem = fila_pedidos.get()
        pedido = mensagem
        sabor = pedido["sabor"]
        cliente = pedido["cliente"]
        total_pedido = pedido["total"]

        dados_por_sabor = verifica_estoque(sabor)

        if dados_por_sabor is None:
            print(f"Sabor '{sabor}' não encontrado no estoque.")
            continue

        quantidade, preco_unitario = dados_por_sabor

        if quantidade < total_pedido:
            print(f"Estoque insuficiente para o sabor '{sabor}'.")
            continue

        total = preco_unitario * total_pedido
        pedido["total"] = total 
        
        #salva pedido no banco
        salvar_pedido(pedido)

        qtd_restante = quantidade - total_pedido
        
        #atualiza o estoque
        atualiza_estoque(sabor, qtd_restante)    
         
        #aqui deveria ser uma notificação q o pedido foi aceito sepa        
        print(f"Pedido de {cliente} processado com sucesso. Total: R${total:.2f}")
        