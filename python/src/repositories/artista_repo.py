# src/repositories/artista_repo.py
import pandas as pd
from src.db import get_engine, get_psycopg2_conn

def listar_todos():
    engine = get_engine()
    return pd.read_sql_query(
        "SELECT * FROM artista ORDER BY id_artista;",
        engine
    )

def consultar(nome: str = "", cpf_rg: str = "", email: str = ""):
    engine = get_engine()
    query = """
        SELECT *
        FROM artista
        WHERE (%(nome)s = '' OR nome ILIKE %(nome_like)s)
          AND (%(cpf)s = '' OR cpf_rg ILIKE %(cpf_like)s)
          AND (%(email)s = '' OR email ILIKE %(email_like)s)
        ORDER BY id_artista;
    """
    params = {
        "nome": nome or "",
        "nome_like": f"%{nome}%",
        "cpf": cpf_rg or "",
        "cpf_like": f"%{cpf_rg}%",
        "email": email or "",
        "email_like": f"%{email}%"
    }
    return pd.read_sql_query(query, engine, params=params)

def inserir(nome, cpf_rg, email, numero, descricao):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO artista (nome, cpf_rg, email, numero, descricao)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome, cpf_rg, email, numero, descricao),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def atualizar(id_artista, nome, cpf_rg, email, numero, descricao):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE artista
               SET nome=%s, cpf_rg=%s, email=%s, numero=%s, descricao=%s
             WHERE id_artista=%s
            """,
            (nome, cpf_rg, email, numero, descricao, id_artista),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def excluir(id_artista):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM artista WHERE id_artista=%s", (id_artista,))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

# ---------- Agregação para gráfico ----------
def top_artistas_por_eventos(limit: int = 10):
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT a.nome AS artista, COUNT(*) AS total_eventos
        FROM artista_participa_evento ae
        JOIN artista a ON a.id_artista = ae.id_artista
        GROUP BY a.nome
        ORDER BY total_eventos DESC
        LIMIT %(limit)s;
        """,
        engine,
        params={"limit": int(limit)}
    )
