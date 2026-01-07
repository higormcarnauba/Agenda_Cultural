# src/repositories/auth_repo.py

from typing import Optional, Dict, Any

from src.repositories.usuario_repo import autenticar as _autenticar
from src.repositories.usuario_repo import hash_senha as _hash_senha


def autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
    """
    Faz login com email e senha.
    Retorna dict do usuário (sem senha_hash) ou None.
    """
    return _autenticar(email, senha)


def hash_senha(senha: str) -> str:
    """
    Gera hash bcrypt para salvar no banco.
    (requer que usuario_repo.hash_senha exista)
    """
    return _hash_senha(senha)


def is_admin(user: Optional[Dict[str, Any]]) -> bool:
    """
    Retorna True se o usuário tiver role de admin.
    Ajuste os nomes conforme sua tabela role (ex.: "Administrador", "Admin", etc.)
    """
    if not user:
        return False
    role = (user.get("role") or "").strip().lower()
    return role in ("administrador", "admin")
