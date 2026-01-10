# src/UTIL/formatters.py

from __future__ import annotations
from datetime import date, datetime
from typing import Any

def str_or_empty(v: Any) -> str:
    """Converte para string, retornando '' para None."""
    return "" if v is None else str(v)

def to_int_or_none(v: Any):
    """Converte para int ou retorna None se vazio/None."""
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        return None

def to_float_or_none(v: Any):
    """Converte para float ou retorna None se vazio/None."""
    if v is None:
        return None
    s = str(v).strip().replace(",", ".")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None

def date_to_yyyy_mm_dd(d: date | datetime | None) -> str:
    """Converte date/datetime para 'YYYY-MM-DD' (ou '' se None)."""
    if d is None:
        return ""
    if isinstance(d, datetime):
        return d.date().isoformat()
    return d.isoformat()

def datetime_to_str(dt: datetime | None) -> str:
    """Converte datetime para string 'YYYY-MM-DD HH:MM:SS' (ou '' se None)."""
    if dt is None:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def money_br(v: Any) -> str:
    """Formata número como moeda BR simples: 1234.5 -> 'R$ 1.234,50'."""
    try:
        n = float(str(v).replace(",", "."))
    except Exception:
        return "R$ 0,00"
    # formata estilo pt-BR sem depender de locale do SO
    s = f"{n:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"
