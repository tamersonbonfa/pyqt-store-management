# services/usuario_service.py
from __future__ import annotations
from typing import Any
from database.db import get_connection
from datetime import datetime
import hashlib

def _hash_senha(senha: str) -> str:
    """Gera hash da senha usando SHA256."""
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def listar_usuarios() -> list[dict[str, Any]]:
    """Retorna todos os usuários."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, username, nome, is_admin, ativo
            FROM usuarios
            ORDER BY username COLLATE NOCASE ASC
        """).fetchall()
        return [dict(r) for r in rows]


def buscar_usuario_por_id(usuario_id: int) -> dict[str, Any] | None:
    """Busca um usuário pelo ID."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, username, nome, is_admin, ativo
            FROM usuarios
            WHERE id = ?
        """, (usuario_id,)).fetchone()
        return dict(row) if row else None


def criar_usuario(username: str, nome: str, senha: str, is_admin: bool = False, ativo: bool = True) -> int:
    """Cria um novo usuário."""
    if not username or not nome or not senha:
        raise ValueError("Username, nome e senha são obrigatórios.")

    senha_hash = _hash_senha(senha)

    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO usuarios (username, nome, senha_hash, is_admin, ativo, criado_em)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, nome, senha_hash, 1 if is_admin else 0, 1 if ativo else 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return int(cur.lastrowid)


def atualizar_usuario(usuario_id: int, username: str, nome: str, senha: str | None = None, is_admin: bool = False, ativo: bool = True):
    """Atualiza um usuário existente. Se senha for None, não altera a senha."""
    if not username or not nome:
        raise ValueError("Username e nome são obrigatórios.")

    with get_connection() as conn:
        if senha:
            senha_hash = _hash_senha(senha)
            conn.execute("""
                UPDATE usuarios
                SET username = ?, nome = ?, senha_hash = ?, is_admin = ?, ativo = ?
                WHERE id = ?
            """, (username, nome, senha_hash, 1 if is_admin else 0, 1 if ativo else 0, usuario_id))
        else:
            conn.execute("""
                UPDATE usuarios
                SET username = ?, nome = ?, is_admin = ?, ativo = ?
                WHERE id = ?
            """, (username, nome, 1 if is_admin else 0, 1 if ativo else 0, usuario_id))
        conn.commit()


def autenticar_usuario(username: str, senha: str) -> dict[str, Any] | None:
    """Verifica login e retorna dados do usuário se correto."""
    senha_hash = _hash_senha(senha)
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, username, nome, is_admin, ativo
            FROM usuarios
            WHERE username = ? AND senha_hash = ? AND ativo = 1
        """, (username, senha_hash)).fetchone()
        return dict(row) if row else None
