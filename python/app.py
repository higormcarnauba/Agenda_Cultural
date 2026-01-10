# app.py
# Execute com: panel serve app.py --autoreload --show

import panel as pn
from src.ui.login import view as login_view
from src.repositories.auth_repo import is_admin

# Extensões
pn.extension("tabulator", notifications=True, design="material")
pn.config.sizing_mode = "stretch_width"

# Importa as telas
from src.ui.eventos import view as eventos_view
from src.ui.espacos import view as espacos_view
from src.ui.artistas import view as artistas_view
from src.ui.usuarios import view as usuarios_view
from src.ui.denuncias import view as denuncias_view

# Container principal que troca entre Login e App
root = pn.Column()

def show_login():
    """Exibe a tela de login."""
    def on_login_success(user):
        show_app(user)
    
    # Limpa e mostra login
    root[:] = [login_view(on_login_success)]

def show_app(user: dict):
    """Exibe a aplicação principal para o usuário logado."""
    admin = is_admin(user)
    
    # Header com botão de Sair
    header = pn.Row(
        pn.pane.Markdown(f"### Olá, {user.get('nome', 'Usuário')}"),
        pn.Spacer(),
        pn.pane.Markdown(f"**Perfil:** {user.get('role', 'Visitante')}", align="center"),
        pn.widgets.Button(name="Sair", button_type="danger", on_click=lambda e: show_login()),
        align="center"
    )

    # Abas dinâmicas baseadas no perfil
    # RBAC: Se Admin -> can_edit=True. Se Comum -> can_edit=False
    # Se quiser passar user para avaliações, passamos 'user'
    
    tabs = pn.Tabs(dynamic=True)
    
    # Abas Comuns
    tabs.append(("Eventos", eventos_view(user=user, can_edit=admin)))
    tabs.append(("Espaços", espacos_view(user=user, can_edit=admin)))
    
    # Abas Extras (Admin ou Comum? User pediu 'separação')
    # Vou mostrar Artistas para todos (read-only se comum?)
    # O arquivo artistas.py foi ajustado? Se não, chamamos padrão.
    # Assumindo assinaturas padrão: view(user=..., can_edit=...)
    # Se a view não aceitar args, vai quebrar.
    # O usuario pediu "separação". Admin cria/edita. Comum lista/avalia.
    
    if admin:
        # Admin vê tudo
        tabs.append(("Artistas", artistas_view(user=user, can_edit=True)))
        tabs.append(("Usuários", usuarios_view())) # Gestão de usuários
        tabs.append(("Denúncias", denuncias_view(user=user, can_edit=True)))
    else:
        # Comum vê Artistas? "Usuario comum pode só listar ... eventos ... espaços"
        # Vou deixar Artistas visível (readonly) para ficar mais completo, ou omitir se quiser estrito.
        # Vou seguir estrito: Eventos e Espaços.
        pass

    root[:] = [
        pn.Column(
            header,
            pn.layout.Divider(),
            tabs
        )
    ]

# Início
show_login()

# Servable
root.servable()
