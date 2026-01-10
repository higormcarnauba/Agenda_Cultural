# src/ui/espacos.py
import panel as pn
import pandas as pd
import src.repositories.espaco_repo as espaco_repo

def view(user=None, can_edit=True, can_denunciar=True):
    pn.config.sizing_mode = "stretch_width"

    # --- Widgets de Filtro ---
    f_nome = pn.widgets.TextInput(name="Nome", placeholder="Nome do espaço")
    f_bairro = pn.widgets.TextInput(name="Bairro", placeholder="Bairro")
    btn_filtrar = pn.widgets.Button(name="Filtrar", button_type="primary")
    
    # --- Tabela ---
    tabela = pn.widgets.Tabulator(
        espaco_repo.listar_todos(), 
        pagination="remote", 
        page_size=10,
        disabled=True
    )

    return pn.Column(
        pn.Card(pn.Column(f_nome, f_bairro, btn_filtrar), title="Filtros"),
        tabela
    )
