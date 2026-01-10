# app.py
# panel serve app.py --autoreload --show

import panel as pn
pn.extension("tabulator", notifications=True)
pn.config.sizing_mode = "stretch_width"

from src.ui.login import view as login_view

from src.ui.eventos import view as eventos_view
from src.ui.espacos import view as espacos_view
from src.ui.artistas import view as artistas_view
from src.ui.usuarios import view as usuarios_view
from src.ui.denuncias import view as denuncias_view


def is_admin(user: dict) -> bool:
    role = (user.get("role") or "").strip().lower()
    return role in ("administrador", "admin")


root = pn.Column()  # container que troca login/app


def show_login():
    def on_success(user):
        show_app(user)
    root[:] = [login_view(on_success)]


def show_app(user: dict):
    admin = is_admin(user)

    header = pn.Row(
        pn.pane.Markdown(f"**Logado:** {user.get('nome')}  \n**Role:** {user.get('role')}"),
        pn.Spacer(),
        pn.widgets.Button(name="Sair", button_type="danger"),
    )

    btn_logout = header[2]
    btn_logout.on_click(lambda _: show_login())

    # ✅ ABAS DIFERENTES POR PERFIL
    if admin:
        tabs = pn.Tabs(
            ("Eventos", eventos_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Espaços", espacos_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Artistas", artistas_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Usuários", usuarios_view(user=user, can_edit=True,  can_denunciar=False)),
            ("Denúncias", denuncias_view(user=user, can_edit=True, can_denunciar=True)),
            dynamic=True,
        )
    else:
        tabs = pn.Tabs(
            ("Eventos", eventos_view(user=user, can_edit=False, can_denunciar=False)),
            ("Artistas", artistas_view(user=user, can_edit=False, can_denunciar=False)),
            ("Denúncias", denuncias_view(user=user, can_edit=False, can_denunciar=True)),
            dynamic=True,
        )

    root[:] = [pn.Column(header, tabs)]


show_login()
root.servable()
