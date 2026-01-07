# src/repositories/denucia_repo.py
import pandas as pd
from src.db import get_engine, get_psycopg2_conn

def listar_todos():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT d.*,
               u.nome AS usuario_nome,
               e.titulo AS evento_titulo
        FROM usuario_denuncia_evento d
        JOIN usuario u ON u.id_usuario = d.id_usuario
        JOIN evento e ON e.id_evento = d.id_evento
        ORDER BY d.id_denuncia DESC;
        """,
        engine
    )

def consultar(status: str = "", motivo: str = "", data_de: str = "", data_ate: str = ""):
    engine = get_engine()
    query = """
        SELECT d.*,
               u.nome AS usuario_nome,
               e.titulo AS evento_titulo
        FROM usuario_denuncia_evento d
        JOIN usuario u ON u.id_usuario = d.id_usuario
        JOIN evento e ON e.id_evento = d.id_evento
        WHERE (%(status)s = '' OR d.status = %(status)s)
          AND (%(motivo)s = '' OR d.motivo ILIKE %(motivo_like)s)
          AND (%(data_de)s = '' OR d.data >= (%(data_de)s)::date)
          AND (%(data_ate)s = '' OR d.data <= (%(data_ate)s)::date + interval '1 day' - interval '1 second')
        ORDER BY d.id_denuncia DESC;
    """
    params = {
        "status": status or "",
        "motivo": motivo or "",
        "motivo_like": f"%{motivo}%",
        "data_de": data_de or "",
        "data_ate": data_ate or "",
    }
    return pd.read_sql_query(query, engine, params=params)

def inserir(id_usuario, id_evento, motivo, descricao, status):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO usuario_denuncia_evento (id_usuario, id_evento, motivo, descricao, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_usuario, id_evento, motivo, descricao, status),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def atualizar(id_denuncia, id_usuario, id_evento, motivo, descricao, status):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE usuario_denuncia_evento
               SET id_usuario=%s,
                   id_evento=%s,
                   motivo=%s,
                   descricao=%s,
                   status=%s
             WHERE id_denuncia=%s
            """,
            (id_usuario, id_evento, motivo, descricao, status, id_denuncia),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def excluir(id_denuncia):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM usuario_denuncia_evento WHERE id_denuncia=%s", (id_denuncia,))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

# ---------- Agregação para gráfico ----------
def denuncias_por_status():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT status, COUNT(*) AS total
        FROM usuario_denuncia_evento
        GROUP BY status
        ORDER BY total DESC;
        """,
        engine
    )
