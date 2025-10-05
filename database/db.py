import sqlite3
from pathlib import Path
import json

DB_PATH = "brigadeiro.db"
JSON_PATH = "./database/estoque.json"

def popular_banco():
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
        cursor.execute("INSERT INTO pedidos (cliente, status, total, sabor) VALUES (?, ?, ?, ?)", (pedido["cliente"], "pendente", 0, pedido["sabor"]))
        conn.commit()
        id = cursor.lastrowid
        pedido = cursor.execute("SELECT * FROM pedidos WHERE id = ?", (id,)).fetchone()
        return pedido_dict(pedido)

def pedido_dict(pedido):
    if pedido is None:
        return None
    return {
        "id": pedido[0],
        "cliente": pedido[1],
        "status": pedido[2]
    }