# src/ui/eventos.py
import panel as pn
import pandas as pd
import src.repositories.evento_repo as evento_repo
import src.repositories.espaco_repo as espaco_repo

def view(user=None, can_edit=True, can_denunciar=True):
    # Mantendo assinatura flexível para compatibilidade futura, mas ignorando auth por agora
    pn.config.sizing_mode = "stretch_width"

    # --- Setup de Dados (Combos) ---
    df_espacos = espaco_repo.listar_para_select()
    mapa_espacos = {}
    if df_espacos is not None and not df_espacos.empty:
        mapa_espacos = {row["nome"]: row["id_espaco_cult"] for _, row in df_espacos.iterrows()}

    # --- Área de Filtros ---
    f_titulo = pn.widgets.TextInput(name="Título", placeholder="Buscar...")
    f_cat = pn.widgets.TextInput(name="Categoria")
    f_espaco = pn.widgets.Select(name="Espaço", options=[""] + list(mapa_espacos.keys()))
    btn_filtrar = pn.widgets.Button(name="Filtrar", button_type="primary")

    # --- Tabela Principal ---
    df_inicial = evento_repo.listar_todos()
    
    tabela = pn.widgets.Tabulator(
        df_inicial,
        pagination="remote",
        page_size=10,
        disabled=True, 
        layout="fit_columns"
    )

    # --- Layout Simples (Sem lógica complexa de user ainda) ---
    return pn.Column(
        pn.Card(pn.Column(f_titulo, f_cat, f_espaco, btn_filtrar), title="Filtros"),
        pn.pane.Markdown("### Lista de Eventos"),
        tabela
    )
