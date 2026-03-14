from __future__ import annotations

from database.db import get_connection


def get_config(chave: str, default: str = "") -> str:
    chave = (chave or "").strip()
    if not chave:
        return default

    with get_connection() as conn:
        row = conn.execute(
            "SELECT valor FROM configuracoes WHERE chave = ?",
            (chave,),
        ).fetchone()

        if not row:
            return default

        return str(row["valor"])


def set_config(chave: str, valor: str) -> None:
    chave = (chave or "").strip()
    valor = str(valor)

    if not chave:
        return

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO configuracoes (chave, valor)
            VALUES (?, ?)
            ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor
            """,
            (chave, valor),
        )
        conn.commit()
