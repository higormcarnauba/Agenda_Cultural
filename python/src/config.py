import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"  # raiz do projeto (mesma pasta do app.py)
load_dotenv(dotenv_path=ENV_PATH, override=True)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")


def validate_env():
    """Valida se as variáveis mínimas do banco foram informadas."""
    missing = []
    if not DB_NAME:
        missing.append("DB_NAME")
    if not DB_USER:
        missing.append("DB_USER")
    if not DB_PASS:
        missing.append("DB_PASS")

    if missing:
        raise RuntimeError(
            "Variáveis ausentes no .env: " + ", ".join(missing) +
            "\nCrie um arquivo .env (não suba pro Git) ou ajuste o .env.example."
        )

def sqlalchemy_url() -> str:
    """
    URL para SQLAlchemy engine.
    Usamos postgresql+psycopg2 para garantir o driver.
    """
    validate_env()
    return f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
