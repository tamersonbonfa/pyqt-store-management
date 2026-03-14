import sqlite3
import random
from datetime import datetime, timedelta

def injetar_dados():
    # Conecta ao seu banco existente
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()
    agora = datetime.now()

    print("🌱 Iniciando inserção de dados em 'database.db'...")

    try:
        # 1. Buscar IDs de usuários existentes para não dar erro de FK
        user_rows = cursor.execute("SELECT id, nome FROM usuarios WHERE ativo = 1").fetchall()
        if not user_rows:
            print("❌ Erro: Nenhum usuário ativo encontrado. Cadastre um usuário no app primeiro.")
            return
        
        user_ids = [row[0] for row in user_rows]
        user_nomes = {row[0]: row[1] for row in user_rows}

        # 2. Criar alguns produtos de teste (se não houver muitos)
        categorias = ["Body Splash", "Condicionador", "Desodorante", "Máscara", "Perfume", "Sabonete", "Shampo"]
        for i in range(10):
            nome = f"Produto Teste {random.randint(100, 999)}"
            cursor.execute("""
                INSERT INTO produtos (nome, marca, custo, preco_venda, quantidade, estoque_minimo, criado_em, categoria, tamanho, unidade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, "Marca Teste", 25.0, 60.0, 20, 5, agora.isoformat(), random.choice(categorias), 100.0, "ml"))
        
        prod_ids = [r[0] for r in cursor.execute("SELECT id FROM produtos").fetchall()]

        # 3. Gerar Movimentações e Vendas (Últimos 30 dias)
        for _ in range(50):
            dias_atras = random.randint(0, 30)
            dt_obj = agora - timedelta(days=dias_atras)
            data_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
            
            p_id = random.choice(prod_ids)
            u_id = random.choice(user_ids)
            u_nome = user_nomes[u_id]
            qtd = random.randint(1, 5)
            
            # Pegar dados do produto para garantir consistência
            p_info = cursor.execute("SELECT preco_venda, tamanho, unidade FROM produtos WHERE id=?", (p_id,)).fetchone()
            preco, tam, uni = p_info

            # Simular uma SAÍDA (Venda)
            tipo = random.choice(["ENTRADA", "SAIDA", "AJUSTE"])
            
            v_id = None
            total_venda = 0
            if tipo == "SAIDA":
                total_venda = preco * qtd
                # Inserir na tabela vendas
                cursor.execute("""
                    INSERT INTO vendas (data, cliente_id, usuario_id, forma_pagamento, total, valor_pago, troco)
                    VALUES (?, NULL, ?, ?, ?, ?, 0)
                """, (data_str, u_id, random.choice(["PIX", "DINHEIRO", "CARTAO"]), total_venda, total_venda))
                v_id = cursor.lastrowid

            # Inserir na tabela movimentacoes_estoque (respeitando seu schema)
            cursor.execute("""
                INSERT INTO movimentacoes_estoque 
                (data, tipo, produto_id, quantidade, observacao, usuario_id, usuario_nome, venda_id, valor_venda, tamanho, unidade)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (data_str, tipo, p_id, qtd, f"Teste de Categoria {tipo}", u_id, u_nome, v_id, total_venda, tam, uni))

        conn.commit()
        print(f"✅ Sucesso! 50 movimentações injetadas vinculadas aos seus usuários.")

    except sqlite3.Error as e:
        print(f"❌ Erro de banco de dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    injetar_dados()