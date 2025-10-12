import sqlite3
from pathlib import Path
import json

DB_PATH = "brigadeiro.db"
JSON_PATH = "brigadeiro-gourmet\database\estoque.json"

def popular_banco():
    print("Entrou em popular banco")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY,
            sabor TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            ingredientes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            status VARCHAR NOT NULL,
            data_pedido TEXT DEFAULT CURRENT_TIMESTAMP,
            total REAL,
            sabor TEXT
        )
        """)

        if Path(JSON_PATH).exists():
            print("qualquercoisa")
            
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                estoque_data = json.load(f)

            for item in estoque_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO estoque (id, sabor, quantidade, preco_unitario, ingredientes)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    item["id"],
                    item["sabor"],
                    item["quantidade"],
                    item["preco_unitario"],
                    json.dumps(item["ingredientes"], ensure_ascii=False)
                ))

            conn.commit()


def salvar_pedido(pedido):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (cliente, status, total, sabor) VALUES (?, ?, ?, ?)", (pedido["cliente"], "pendente", pedido["total"], pedido["sabor"]))
        conn.commit()
        id = cursor.lastrowid
        pedido = cursor.execute("SELECT * FROM pedidos WHERE id = ?", (id,)).fetchone()
        return 
    
    
    
def ver_pedidos():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        pedidos = cursor.execute("SELECT * FROM pedidos").fetchall()
        conn.commit()
    return [dict(p) for p in pedidos]

def ver_estoque():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        estoque = cursor.execute("SELECT * FROM estoque").fetchall()
        conn.commit()
    return [dict(p) for p in estoque]
        
    
      
def pedido_dict(pedido):
    if pedido is None:
        return None
    return {
        "id": pedido[0],
        "cliente": pedido[1],
        "status": pedido[2]
    }
    
    

def verifica_estoque(sabor):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade, preco_unitario FROM estoque WHERE sabor = ?", (sabor,))
        resultado = cursor.fetchone()
    return resultado
        
        
def atualiza_estoque(sabor, qtd_restante):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE estoque SET quantidade = ? WHERE sabor = ?", (qtd_restante, sabor))
        conn.commit()


def limpa_tabela_pedidos():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Apaga todos os registros da tabela
        cursor.execute("DELETE FROM pedidos")
        
        # Reseta o contador de autoincremento (opcional)
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='pedidos'")
        
        conn.commit()
