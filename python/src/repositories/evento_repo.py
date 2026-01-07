# src/repositories/evento_repo.py
import pandas as pd
from src.db import get_engine, get_psycopg2_conn

def listar_todos():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT ev.*,
               ec.nome AS espaco_nome
        FROM evento ev
        JOIN espaco_cultural ec ON ec.id_espaco_cult = ev.id_espaco_cult
        ORDER BY ev.id_evento;
        """,
        engine,
    )

def consultar(
    titulo: str = "",
    categoria: str = "",
    status: str = "",
    id_espaco_cult: int | None = None,
    data_inicio_de: str = "",
    data_inicio_ate: str = "",
):
    """
    Consulta com filtros opcionais:
    - titulo (ILIKE)
    - categoria (ILIKE)
    - status (igual)
    - id_espaco_cult (igual)
    - intervalo de data_inicio (>= e <=) usando strings 'YYYY-MM-DD'
    """
    engine = get_engine()

    query = """
        SELECT ev.*,
               ec.nome AS espaco_nome
        FROM evento ev
        JOIN espaco_cultural ec ON ec.id_espaco_cult = ev.id_espaco_cult
        WHERE (%(titulo)s = '' OR ev.titulo ILIKE %(titulo_like)s)
          AND (%(categoria)s = '' OR ev.categoria ILIKE %(categoria_like)s)
          AND (%(status)s = '' OR ev.status = %(status)s)
          AND (%(id_espaco_cult)s IS NULL OR ev.id_espaco_cult = %(id_espaco_cult)s)
          AND (%(data_de)s = '' OR ev.data_inicio >= (%(data_de)s)::date)
          AND (%(data_ate)s = '' OR ev.data_inicio <= (%(data_ate)s)::date + interval '1 day' - interval '1 second')
        ORDER BY ev.id_evento;
    """

    params = {
        "titulo": titulo or "",
        "titulo_like": f"%{titulo}%",
        "categoria": categoria or "",
        "categoria_like": f"%{categoria}%",
        "status": status or "",
        "id_espaco_cult": id_espaco_cult,
        "data_de": data_inicio_de or "",
        "data_ate": data_inicio_ate or "",
    }

    return pd.read_sql_query(query, engine, params=params)

def inserir(titulo, descricao, categoria, capacidade, data_inicio, data_fim, preco, status, id_espaco_cult):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO evento
                (titulo, descricao, categoria, capacidade, data_inicio, data_fim, preco, status, id_espaco_cult)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (titulo, descricao, categoria, capacidade, data_inicio, data_fim, preco, status, id_espaco_cult),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def atualizar(id_evento, titulo, descricao, categoria, capacidade, data_inicio, data_fim, preco, status, id_espaco_cult):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute(
            """
            UPDATE evento
               SET titulo=%s,
                   descricao=%s,
                   categoria=%s,
                   capacidade=%s,
                   data_inicio=%s,
                   data_fim=%s,
                   preco=%s,
                   status=%s,
                   id_espaco_cult=%s
             WHERE id_evento=%s
            """,
            (titulo, descricao, categoria, capacidade, data_inicio, data_fim, preco, status, id_espaco_cult, id_evento),
        )
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def excluir(id_evento):
    con = get_psycopg2_conn()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM evento WHERE id_evento=%s", (id_evento,))
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

# ---------- Agregação para gráfico ----------
def eventos_por_mes():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT DATE_TRUNC('month', data_inicio) AS mes,
               COUNT(*) AS total
        FROM evento
        GROUP BY mes
        ORDER BY mes;
        """,
        engine
    )

def eventos_por_categoria():
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT COALESCE(categoria, 'Sem categoria') AS categoria,
               COUNT(*) AS total
        FROM evento
        GROUP BY COALESCE(categoria, 'Sem categoria')
        ORDER BY total DESC;
        """,
        engine
    )
