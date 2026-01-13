# app.py
# panel serve app.py --autoreload --show

import panel as pn
pn.extension("tabulator", notifications=True)
pn.config.sizing_mode = "stretch_width"

from src.ui.login import view as login_view

# Se algum arquivo de tela ainda não existir, comente o import correspondente
from src.ui.eventos import view as eventos_view
from src.ui.espacos import view as espacos_view
from src.ui.artistas import view as artistas_view
from src.ui.usuarios import view as usuarios_view
from src.ui.denuncias import view as denuncias_view

# Se estiver usando auth_repo:
try:
    from src.repositories.auth_repo import is_admin, is_gerente, is_visitante
except Exception:
    def is_admin(_u): return False
    def is_gerente(_u): return False
    def is_visitante(_u): return False


root = pn.Column()  # sempre terá conteúdo


def show_login():
    def on_success(user):
        show_app(user)
    root.objects = [login_view(on_success)]


def show_app(user: dict):
    admin = is_admin(user)
    gerente = is_gerente(user)
    visitante = is_visitante(user)

    header = pn.Row(
        pn.pane.Markdown(f"**Logado:** {user.get('nome')}  \n**Role:** {user.get('role')}"),
        pn.Spacer(),
        pn.widgets.Button(name="Sair", button_type="danger"),
    )
    header[2].on_click(lambda _: show_login())

    # Visitante
    if visitante:
        tabs = pn.Tabs(
            ("Eventos", eventos_view(user=user, can_edit=False, can_denunciar=False)),
            ("Espaços", espacos_view(user=user, can_edit=False, can_denunciar=False)),
            dynamic=True,
        )
    # Comum
    elif (not admin) and (not gerente):
        tabs = pn.Tabs(
            ("Eventos", eventos_view(user=user, can_edit=False, can_denunciar=False)),
            ("Artistas", artistas_view(user=user, can_edit=False, can_denunciar=False)),
            ("Denúncias", denuncias_view(user=user, can_edit=False, can_denunciar=True)),
            dynamic=True,
        )
    # Gerente
    elif gerente and not admin:
        tabs = pn.Tabs(
            ("Eventos", eventos_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Espaços", espacos_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Artistas", artistas_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Usuários", usuarios_view(user=user, can_edit=True, can_denunciar=False)),
            dynamic=True,
        )
    # Admin
    else:
        tabs = pn.Tabs(
            ("Eventos", eventos_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Espaços", espacos_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Artistas", artistas_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Usuários", usuarios_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Denúncias", denuncias_view(user=user, can_edit=True, can_denunciar=True)),
            dynamic=True,
        )

    root.objects = [pn.Column(header, tabs)]


# ✅ SEMPRE chama isso, para publicar algo
show_login()

# ✅ SEMPRE marca como servable
root.servable()
