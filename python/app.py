# app.py
# Execute com: panel serve app.py --autoreload --show

import panel as pn

# Extensões do Panel (Tabulator + notificações)
pn.extension("tabulator", notifications=True)

# Importa as telas (cada arquivo deve ter uma função view() que retorna um layout Panel)
from src.ui.eventos import view as eventos_view
from src.ui.espacos import view as espacos_view
from src.ui.artistas import view as artistas_view
from src.ui.usuarios import view as usuarios_view
from src.ui.denuncias import view as denuncias_view

# (Opcional) configurações globais de layout
pn.config.sizing_mode = "stretch_width"

# Monta as abas (5 telas)
# Nota: Passamos as views simples, sem argumentos de usuario por enquanto
app = pn.Tabs(
    ("Eventos", eventos_view()),
    ("Espaços", espacos_view()),
    ("Artistas", artistas_view()),
    ("Usuários", usuarios_view()),
    ("Denúncias", denuncias_view()),
    dynamic=True,
)

# Deixa servível pelo panel serve
app.servable()
