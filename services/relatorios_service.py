from __future__ import annotations
from typing import Any
from database.db import get_connection # Ou use o seu db_manager

class RelatoriosService:
    @staticmethod
    def resumo_detalhado(inicio: str, fim: str) -> dict[str, Any]:
        """Busca métricas financeiras, ranking de produtos e alertas de estoque."""
        with get_connection() as conn:
            # 1. Resumo Financeiro do Período
            financeiro = conn.execute("""
                SELECT 
                    COUNT(id) as total_vendas,
                    SUM(total) as faturamento,
                    CASE WHEN COUNT(id) > 0 THEN SUM(total) / COUNT(id) ELSE 0 END as ticket_medio
                FROM vendas 
                WHERE date(data) BETWEEN date(?) AND date(?)
            """, (inicio, fim)).fetchone()
            
            # 2. Vendas por Forma de Pagamento
            pagamentos = conn.execute("""
                SELECT forma_pagamento, SUM(total) as total
                FROM vendas
                WHERE date(data) BETWEEN date(?) AND date(?)
                GROUP BY forma_pagamento
            """, (inicio, fim)).fetchall()

            # 3. Ranking de Produtos Detalhado
            produtos = conn.execute("""
                SELECT 
                    p.nome, 
                    p.tamanho,
                    p.unidade,
                    p.custo as preco_compra,
                    p.preco_venda,
                    SUM(i.quantidade) as qtd_vendida, 
                    SUM(i.subtotal) as total_faturado,
                    SUM( (i.preco_unitario * i.quantidade) * (i.desconto / 100.0) ) as desconto_total_reais,
                    (SUM(i.subtotal) - SUM(i.quantidade * p.custo)) as lucro_estimado
                FROM venda_itens i
                JOIN produtos p ON p.id = i.produto_id
                JOIN vendas v ON v.id = i.venda_id
                WHERE date(v.data) BETWEEN date(?) AND date(?)
                GROUP BY p.id 
                ORDER BY total_faturado DESC
            """, (inicio, fim)).fetchall()

            # 4. Alerta de Estoque Crítico
            estoque_baixo = conn.execute("""
                SELECT nome, quantidade, estoque_minimo 
                FROM produtos 
                WHERE quantidade <= estoque_minimo AND ativo = 1
                ORDER BY quantidade ASC LIMIT 15
            """).fetchall()

            return {
                "financeiro": dict(financeiro) if financeiro and financeiro["total_vendas"] else None,
                "pagamentos": [dict(r) for r in pagamentos],
                "produtos": [dict(r) for r in produtos],
                "estoque_baixo": [dict(r) for r in estoque_baixo]
            }
    
    @staticmethod
    def obter_relatorio_movimentacoes() -> list[dict]:
            """
            Retorna os dados usando a função que já funciona na sua interface principal.
            Isso garante que usaremos a tabela correta.
            """
            try:
                # Importamos a função que você já usa para preencher o "Histórico: Geral"
                from services.produtos_service import listar_movimentacoes
                
                # Chamamos ela pedindo um limite maior para o relatório
                dados = listar_movimentacoes(limite=2000)
                
                # Como a sua tabela de relatório pede nomes de colunas específicos, 
                # garantimos a compatibilidade aqui:
                formatados = []
                for d in dados:
                    formatados.append({
                        "data": d.get("data"),
                        "tipo": d.get("tipo"),
                        "produto": d.get("produto_nome"), # Pegando o nome do produto que já vem do JOIN
                        "quantidade": d.get("quantidade"),
                        "observacao": d.get("observacao"),
                        "usuario": d.get("usuario_nome")  # Pegando o nome do usuário
                    })
                return formatados
            except Exception as e:
                print(f"Erro ao carregar dados do service existente: {e}")
                return []