# src/repositories/espaco_repo.py
import pandas as pd
from src.db import get_engine, get_psycopg2_conn

def listar_todos():
    engine = get_engine()
    return pd.read_sql_query(
        "SELECT * FROM espaco_cultural ORDER BY id_espaco_cult;",
        engine
    )

def listar_para_select():
    """Retorna somente id e nome (para dropdown em eventos)."""
    engine = get_engine()
    return pd.read_sql_query(
        "SELECT id_espaco_cult, nome FROM espaco_cultural ORDER BY nome;",
        engine
    )

def consultar(nome: str = "", bairro: str = ""):
    engine = get_engine()
    query = """
        SELECT *
        FROM espaco_cultural
        WHERE (%(nome)s = '' OR nome ILIKE %(nome_like)s)
          AND (%(bairro)s = '' OR bairro ILIKE %(bairro_like)s)
        ORDER BY id_espaco_cult;
    """
    params = {
        "nome": nome or "",
        "nome_like": f"%{nome}%",
        "bairro": bairro or "",
        "bairro_like": f"%{bairro}%"
    }
    return pd.read_sql_query(query, engine, params=params)

def inserir(nome, rua, numero, bairro):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO espaco_cultural (nome, rua, numero, bairro) VALUES (%s, %s, %s, %s)",
            (nome, rua, numero, bairro),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def atualizar(id_espaco_cult, nome, rua, numero, bairro):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE espaco_cultural
               SET nome=%s, rua=%s, numero=%s, bairro=%s
             WHERE id_espaco_cult=%s
            """,
            (nome, rua, numero, bairro, id_espaco_cult),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def excluir(id_espaco_cult):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            "DELETE FROM espaco_cultural WHERE id_espaco_cult=%s",
            (id_espaco_cult,),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def total_eventos_por_espaco():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT e.nome AS espaco, COUNT(ev.id_evento) AS total_eventos
        FROM espaco_cultural e
        LEFT JOIN evento ev ON ev.id_espaco_cult = e.id_espaco_cult
        GROUP BY e.nome
        ORDER BY total_eventos DESC;
        """,
        engine
    )
