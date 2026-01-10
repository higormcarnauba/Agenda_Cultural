# src/repositories/avaliacao_repo.py
import pandas as pd
from src.db import get_engine, get_psycopg2_conn

def listar_por_evento(id_evento):
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT ae.*, u.nome as usuario_nome
        FROM avaliacao_evento ae
        JOIN usuario u ON u.id_usuario = ae.id_usuario
        WHERE ae.id_evento = %(id_evento)s
        ORDER BY ae.id_avaliacao DESC;
        """,
        engine,
        params={"id_evento": int(id_evento)}
    )

def listar_por_espaco(id_espaco_cult):
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT ae.*, u.nome as usuario_nome
        FROM avaliacao_espaco ae
        JOIN usuario u ON u.id_usuario = ae.id_usuario
        WHERE ae.id_espaco_cult = %(id_espaco_cult)s
        ORDER BY ae.id_avaliacao DESC;
        """,
        engine,
        params={"id_espaco_cult": int(id_espaco_cult)}
    )

def inserir_evento(id_evento, id_usuario, nota, comentario):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO avaliacao_evento (id_evento, id_usuario, nota, comentario)
            VALUES (%s, %s, %s, %s)
            """,
            (id_evento, id_usuario, nota, comentario)
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def inserir_espaco(id_espaco_cult, id_usuario, nota, comentario):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO avaliacao_espaco (id_espaco_cult, id_usuario, nota, comentario)
            VALUES (%s, %s, %s, %s)
            """,
            (id_espaco_cult, id_usuario, nota, comentario)
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def ja_avaliou_evento(id_evento, id_usuario):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT 1 FROM avaliacao_evento WHERE id_evento=%s AND id_usuario=%s",
            (id_evento, id_usuario)
        )
        return cur.fetchone() is not None
    finally:
        con.close()

def ja_avaliou_espaco(id_espaco_cult, id_usuario):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT 1 FROM avaliacao_espaco WHERE id_espaco_cult=%s AND id_usuario=%s",
            (id_espaco_cult, id_usuario)
        )
        return cur.fetchone() is not None
    finally:
        con.close()
