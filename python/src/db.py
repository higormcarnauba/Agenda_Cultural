# src/db.py
import psycopg2 as pg
from sqlalchemy import create_engine
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, sqlalchemy_url, validate_env

_engine = None

def get_psycopg2_conn():
    """
    Conexão psycopg2 (ideal para INSERT/UPDATE/DELETE com parâmetros).
    Retorna uma conexão nova a cada chamada.
    """
    validate_env()
    return pg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def get_engine():
    """
    Engine SQLAlchemy (ideal para SELECT com pandas.read_sql_query).
    Mantém cache para reutilizar.
    """
    global _engine
    if _engine is None:
        _engine = create_engine(
            sqlalchemy_url(),
            pool_pre_ping=True  # evita erro quando a conexão fica "velha"
        )
    return _engine
