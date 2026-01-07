# src/repositories/usuario_repo.py
import pandas as pd
from src.db import get_engine, get_psycopg2_conn


def listar_roles():
    """
    No seu banco, a FK em usuario é id_papel, então na tabela role a PK também é id_papel.
    Aqui eu retorno id_papel com alias id_role pra não quebrar sua UI atual.
    """
    engine = get_engine()
    return pd.read_sql_query(
        "SELECT id_papel AS id_role, nome FROM role ORDER BY nome;",
        engine
    )


def listar_todos():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT u.*,
               r.nome AS role
        FROM usuario u
        JOIN role r ON r.id_papel = u.id_papel
        ORDER BY u.id_usuario;
        """,
        engine
    )


def consultar(nome: str = "", email: str = "", role_nome: str = ""):
    engine = get_engine()
    query = """
        SELECT u.*,
               r.nome AS role
        FROM usuario u
        JOIN role r ON r.id_papel = u.id_papel
        WHERE (%(nome)s = '' OR u.nome ILIKE %(nome_like)s)
          AND (%(email)s = '' OR u.email ILIKE %(email_like)s)
          AND (%(role)s = '' OR r.nome = %(role)s)
        ORDER BY u.id_usuario;
    """
    params = {
        "nome": nome or "",
        "nome_like": f"%{nome}%",
        "email": email or "",
        "email_like": f"%{email}%",
        "role": role_nome or "",
    }
    return pd.read_sql_query(query, engine, params=params)


def inserir(nome, email, cpf_rg, senha_hash, id_role):
    """
    id_role aqui é na prática o id_papel (PK da tabela role).
    """
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO usuario (nome, email, cpf_rg, senha_hash, id_papel)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome, email, cpf_rg, senha_hash, id_role),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def atualizar(id_usuario, nome, email, cpf_rg, senha_hash, id_role):
    """
    id_role aqui é na prática o id_papel (FK em usuario).
    """
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE usuario
               SET nome=%s,
                   email=%s,
                   cpf_rg=%s,
                   senha_hash=%s,
                   id_papel=%s
             WHERE id_usuario=%s
            """,
            (nome, email, cpf_rg, senha_hash, id_role, id_usuario),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def excluir(id_usuario):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM usuario WHERE id_usuario=%s", (id_usuario,))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def usuarios_por_role():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT r.nome AS role, COUNT(*) AS total
        FROM usuario u
        JOIN role r ON r.id_papel = u.id_papel
        GROUP BY r.nome
        ORDER BY total DESC;
        """,
        engine
    )
