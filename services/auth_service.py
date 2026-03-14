from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime

from database.db import get_connection


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hash_password(password: str) -> str:
    # Simples e funcional (local). Se quiser, depois migramos para bcrypt.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


@dataclass
class Usuario:
    id: int
    username: str
    nome: str | None
    is_admin: bool


def ensure_admin_user():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM usuarios WHERE username = ?",
            ("admin",),
        ).fetchone()

        if row:
            # caso já exista, garante que seja admin
            conn.execute(
                "UPDATE usuarios SET is_admin = 1 WHERE id = ?",
                (row["id"],)
            )
            conn.commit()
            return

        conn.execute(
            """
            INSERT INTO usuarios (username, senha_hash, nome, ativo, is_admin, criado_em)
            VALUES (?, ?, ?, 1, 1, ?)
            """,
            ("admin", hash_password("admin"), "Administrador", _now_iso()),
        )
        conn.commit()


def authenticate(username: str, password: str) -> Usuario | None:
    username = (username or "").strip()

    if not username or not password:
        return None

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, username, nome, senha_hash, is_admin, ativo
            FROM usuarios
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if not row:
            return None

        if int(row["ativo"]) != 1:
            return None

        if row["senha_hash"] != hash_password(password):
            return None

        return Usuario(
            id=int(row["id"]),
            username=str(row["username"]),
            nome=str(row["nome"]),
            is_admin=bool(row["is_admin"]),
        )
