import sqlite3
import bcrypt
import random
import os
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DE CAMINHO ROBUSTA ---
# Pega o caminho absoluto da pasta onde este script (injector.py) está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Monta o caminho correto para database/database.db independente de onde o terminal abrir
DB_NAME = os.path.join(BASE_DIR, "database", "database.db")

def hash_password(password: str) -> str:
    """Gera hash usando bcrypt para ser compatível com o novo sistema."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def _now_iso(days_offset=0):
    """Gera data formatada para o SQLite."""
    dt = datetime.now() + timedelta(days=days_offset)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def inject():
    # Verifica se o banco existe antes de conectar para evitar criar um arquivo vazio errado
    if not os.path.exists(DB_NAME):
        print(f"\n[ERRO] Banco de dados não encontrado em: {DB_NAME}")
        print(f"Verifique se a pasta 'database' existe em: {BASE_DIR}\n")
        return

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    print(f"-> Injetando dados em: {DB_NAME}")

    try:
        # 1. USUÁRIOS (Admin com senha BCrypt)
        # -------------------------------------------------------
        senha_admin = hash_password("admin")
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (username, nome, senha_hash, is_admin, ativo, criado_em)
            VALUES (?, ?, ?, 1, 1, ?)
        """, ("admin", "Administrador", senha_admin, _now_iso(-10)))
        
        # Busca o ID do admin para usar nas chaves estrangeiras
        cursor.execute("SELECT id FROM usuarios WHERE username = 'admin'")
        admin_id = cursor.fetchone()[0]

        # 2. CLIENTES
        # -------------------------------------------------------
        clientes_data = [
            ("Consumidor Final", "0000-0000", "N/A", "Venda balcão", _now_iso(-10)),
            ("João das Couves", "17991234567", "Rua A, 10", "Cliente VIP", _now_iso(-5)),
            ("Maria Silva", "17997654321", "Av B, 200", "Paga sempre no PIX", _now_iso(-2))
        ]
        cursor.executemany("""
            INSERT INTO clientes (nome, telefone, endereco, observacoes, criado_em)
            VALUES (?, ?, ?, ?, ?)
        """, clientes_data)

        # 3. PRODUTOS
        # -------------------------------------------------------
        produtos_data = [
            ("Shampoo Anticaspa", "Clear", 200, 12.50, 28.00, 50, 5, 1, _now_iso(-10), "Higiene", 200.0, "ml", "789123"),
            ("Condicionador", "Dove", 200, 15.00, 32.00, 30, 5, 1, _now_iso(-10), "Higiene", 200.0, "ml", "789456"),
            ("Esmalte Azul", "Risqué", 8, 2.50, 8.50, 100, 10, 1, _now_iso(-10), "Beleza", 8.0, "ml", "789789"),
            ("Corte Masculino", "Serviço", 0, 5.00, 45.00, 999, 0, 1, _now_iso(-10), "Serviço", 0.0, "un", "")
        ]
        cursor.executemany("""
            INSERT INTO produtos (nome, marca, volume_ml, custo, preco_venda, quantidade, estoque_minimo, ativo, criado_em, categoria, tamanho, unidade, codigo_barras)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, produtos_data)

        # 4. VENDAS E ITENS
        # -------------------------------------------------------
        formas = ["DINHEIRO", "PIX", "CARTAO"]
        
        for i in range(1, 6): # Gera 5 vendas aleatórias
            data_v = _now_iso(-random.randint(0, 4))
            forma = random.choice(formas)
            total = 60.0 
            
            cursor.execute("""
                INSERT INTO vendas (data, cliente_id, usuario_id, forma_pagamento, total, valor_pago, troco, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (data_v, random.randint(1, 3), admin_id, forma, total, total, 0.0, "Venda de teste"))
            
            venda_id = cursor.lastrowid

            # Item da venda (Vinculado ao primeiro produto inserido)
            cursor.execute("""
                INSERT INTO venda_itens (venda_id, produto_id, quantidade, preco_unitario, subtotal, tamanho, unidade)
                VALUES (?, 1, 2, 30.0, 60.0, 200.0, 'ml')
            """, (venda_id,))

            # 5. MOVIMENTAÇÃO DE ESTOQUE
            # -------------------------------------------------------
            cursor.execute("""
                INSERT INTO movimentacoes_estoque (data, tipo, produto_id, quantidade, observacao, usuario_id, venda_id, valor_venda)
                VALUES (?, 'SAIDA', 1, 2, ?, ?, ?, 60.0)
            """, (data_v, f"Venda #{venda_id}", admin_id, venda_id))

        conn.commit()
        print("--- Injeção concluída com sucesso na base fornecida ---")

    except sqlite3.OperationalError as e:
        print(f"\n[ERRO DE TABELA] {e}")
        print("A tabela 'usuarios' ou outra não existe no banco informado.")
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    inject()