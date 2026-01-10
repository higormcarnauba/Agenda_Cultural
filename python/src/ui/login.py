# src/ui/login.py
import panel as pn
from src.repositories.auth_repo import autenticar


def view(on_success):
    titulo = pn.pane.Markdown("## Login")

    email = pn.widgets.TextInput(name="Email", placeholder="seuemail@dominio.com")
    senha = pn.widgets.PasswordInput(name="Senha", placeholder="••••••••")
    btn = pn.widgets.Button(name="Entrar", button_type="primary")
    msg = pn.pane.Alert("", alert_type="danger", visible=False)

    def do_login(_):
        user = autenticar(email.value.strip(), senha.value)
        if not user:
            msg.object = "Email ou senha inválidos."
            msg.visible = True
            pn.state.notifications.error("Falha no login", duration=2500)
            return
        msg.visible = False
        on_success(user)

    btn.on_click(do_login)

    return pn.Column(
        pn.Spacer(height=30),
        pn.Row(pn.Spacer(), pn.Column(titulo, email, senha, btn, msg, width=420), pn.Spacer()),
        pn.Spacer(),
    )
