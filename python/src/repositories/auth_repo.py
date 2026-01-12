# src/repositories/auth_repo.py
from typing import Optional, Dict, Any, Iterable
import pandas as pd
from src.db import get_engine
import src.repositories.usuario_repo as usuario_repo

def _norm(s: str) -> str:
    return (s or "").strip().lower()

ADMIN = ("administrador", "admin")
GERENTE = ("gerente",)
COMUM = ("comum", "usuario comum", "usuário comum", "usuario", "usuário")
VISITANTE = ("visitante",)

def autenticar(email: str, senha: str) -> Optional[Dict[str, Any]]:
    return usuario_repo.autenticar(email, senha)

def is_admin(user: Optional[Dict[str, Any]]) -> bool:
    return bool(user) and _norm(user.get("role")) in ADMIN

def is_gerente(user: Optional[Dict[str, Any]]) -> bool:
    return bool(user) and _norm(user.get("role")) in GERENTE

def is_comum(user: Optional[Dict[str, Any]]) -> bool:
    return bool(user) and _norm(user.get("role")) in COMUM

def is_visitante(user: Optional[Dict[str, Any]]) -> bool:
    return (not user) or _norm(user.get("role")) in VISITANTE

# ---- Permissões (use na UI e também no backend/repo) ----
def can_ver_eventos(user: Optional[Dict[str, Any]]) -> bool:
    return True  # visitante também vê

def can_avaliar_ou_denunciar(user: Optional[Dict[str, Any]]) -> bool:
    # pelo teu requisito: usuário comum faz isso.
    # (se quiser permitir gerente/admin também, é só incluir aqui)
    return is_comum(user)

def can_gerenciar(user: Optional[Dict[str, Any]]) -> bool:
    return is_gerente(user) or is_admin(user)

def can_cadastrar_comum(user: Optional[Dict[str, Any]]) -> bool:
    return is_gerente(user) or is_admin(user)

def can_cadastrar_gerente(user: Optional[Dict[str, Any]]) -> bool:
    return is_admin(user)

# ---- util ----
def _buscar_id_papel_por_nomes(nomes: Iterable[str]) -> int:
    engine = get_engine()
    df = pd.read_sql_query("SELECT id_papel, nome FROM role;", engine)
    if df.empty:
        raise ValueError("Tabela role está vazia. Cadastre os papéis primeiro.")
    roles_map = {_norm(n): int(i) for i, n in zip(df["id_papel"], df["nome"])}
    for n in nomes:
        k = _norm(n)
        if k in roles_map:
            return roles_map[k]
    raise ValueError(f"Não encontrei o papel no banco. Tentei: {list(nomes)}")

# ---- Cadastro público (self-signup): sempre COMUM ----
def cadastrar_usuario_comum_publico(nome: str, email: str, cpf_rg: str, senha: str) -> Dict[str, Any]:
    id_papel_comum = _buscar_id_papel_por_nomes(COMUM)
    senha_hash = usuario_repo.hash_senha(senha)  # precisa bcrypt
    usuario_repo.inserir(nome.strip(), email.strip(), cpf_rg.strip(), senha_hash, id_papel_comum)

    user = usuario_repo.autenticar(email.strip(), senha)
    if not user:
        raise RuntimeError("Cadastrou, mas não autenticou (verifique bcrypt/hash).")
    return user

# ---- Cadastro de comum por gerente/admin ----
def cadastrar_usuario_comum_por(ator: Dict[str, Any], nome: str, email: str, cpf_rg: str, senha: str) -> Dict[str, Any]:
    if not can_cadastrar_comum(ator):
        raise PermissionError("Somente GERENTE ou ADMIN pode cadastrar usuário comum.")
    return cadastrar_usuario_comum_publico(nome, email, cpf_rg, senha)

# ---- Cadastro de gerente por admin ----
def cadastrar_gerente_por(ator: Dict[str, Any], nome: str, email: str, cpf_rg: str, senha: str) -> Dict[str, Any]:
    if not can_cadastrar_gerente(ator):
        raise PermissionError("Somente ADMIN pode cadastrar gerente.")
    id_papel_gerente = _buscar_id_papel_por_nomes(GERENTE)
    senha_hash = usuario_repo.hash_senha(senha)
    usuario_repo.inserir(nome.strip(), email.strip(), cpf_rg.strip(), senha_hash, id_papel_gerente)
    user = usuario_repo.autenticar(email.strip(), senha)
    if not user:
        raise RuntimeError("Cadastrou gerente, mas não autenticou (verifique bcrypt/hash).")
    return user
