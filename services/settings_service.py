from __future__ import annotations

from database.db import get_connection


def get_setting(key: str, default: str = "") -> str:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT valor FROM configuracoes WHERE chave = ?",
            (key,),
        ).fetchone()
        return str(row["valor"]) if row else default


def set_setting(key: str, value: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO configuracoes (chave, valor)
            VALUES (?, ?)
            ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor
            """,
            (key, value),
        )
        conn.commit()
