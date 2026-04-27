from __future__ import annotations

import bcrypt
from dataclasses import dataclass
from datetime import datetime

from database.db import get_connection

from config import (
    ADMIN_PWD # IMPORTAR A SENHA DE ADMIN DO CONFIG.PY

)


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hash_password(password: str) -> str:
    # Gera o salt e o hash. O 'cost' padrão é 12.
    # O retorno já inclui o salt necessário para a verificação futura.
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # O bcrypt extrai o salt automaticamente do hash armazenado
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), 
        hashed_password.encode("utf-8")
    )

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
            ("admin", hash_password(ADMIN_PWD), "Administrador", _now_iso()),
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

        if not verify_password(password, row["senha_hash"]):
            return None

        return Usuario(
            id=int(row["id"]),
            username=str(row["username"]),
            nome=str(row["nome"]),
            is_admin=bool(row["is_admin"]),
        )
