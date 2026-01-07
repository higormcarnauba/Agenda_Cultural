# src/repositories/relatorio_repo.py
import pandas as pd
from src.db import get_engine

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

def top_eventos_por_participantes(limit: int = 10):
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT e.titulo AS evento, COUNT(*) AS participantes
        FROM usuario_participa_evento upe
        JOIN evento e ON e.id_evento = upe.id_evento
        GROUP BY e.titulo
        ORDER BY participantes DESC
        LIMIT %(limit)s;
        """,
        engine,
        params={"limit": int(limit)}
    )

def media_nota_por_evento(limit: int = 10):
    engine = get_engine()
    return pd.read_sql_query(
        """
        SELECT e.titulo AS evento, AVG(a.nota) AS media
        FROM usuario_avalia_evento a
        JOIN evento e ON e.id_evento = a.id_evento
        GROUP BY e.titulo
        ORDER BY media DESC
        LIMIT %(limit)s;
        """,
        engine,
        params={"limit": int(limit)}
    )
