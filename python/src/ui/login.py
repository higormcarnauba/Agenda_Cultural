# src/ui/login.py
import panel as pn
from src.repositories.auth_repo import autenticar, cadastrar_usuario_comum

def view(on_success):
    pn.config.sizing_mode = "stretch_width"

    # --- Entrar ---
    l_email = pn.widgets.TextInput(name="Email")
    l_senha = pn.widgets.PasswordInput(name="Senha")
    l_btn = pn.widgets.Button(name="Entrar", button_type="primary")
    l_msg = pn.pane.Alert("", alert_type="danger", visible=False)

    def do_login(_):
        user = autenticar(l_email.value.strip(), l_senha.value)
        if not user:
            l_msg.object = "Email ou senha inválidos."
            l_msg.visible = True
            return
        l_msg.visible = False
        on_success(user)

    l_btn.on_click(do_login)

    login_pane = pn.Column(
        pn.pane.Markdown("## Entrar"),
        l_email, l_senha, l_btn, l_msg,
        width=420
    )

    # --- Cadastrar (sempre como Comum) ---
    c_nome = pn.widgets.TextInput(name="Nome")
    c_email = pn.widgets.TextInput(name="Email")
    c_cpf = pn.widgets.TextInput(name="CPF/RG")
    c_senha = pn.widgets.PasswordInput(name="Senha")
    c_senha2 = pn.widgets.PasswordInput(name="Confirmar senha")
    c_btn = pn.widgets.Button(name="Cadastrar (Usuário comum)", button_type="success")
    c_msg = pn.pane.Alert("", alert_type="danger", visible=False)

    def do_cadastro(_):
        try:
            if c_senha.value != c_senha2.value:
                raise ValueError("As senhas não conferem.")
            user = cadastrar_usuario_comum(c_nome.value, c_email.value, c_cpf.value, c_senha.value)
            c_msg.visible = False
            on_success(user)
        except Exception as e:
            c_msg.object = str(e)
            c_msg.visible = True

    c_btn.on_click(do_cadastro)

    cadastro_pane = pn.Column(
        pn.pane.Markdown("## Não possui cadastro?"),
        c_nome, c_email, c_cpf, c_senha, c_senha2,
        c_btn, c_msg,
        width=420
    )

    # --- Visitante ---
    v_info = pn.pane.Alert(
        "Visitante não precisa de cadastro. Você poderá ver Eventos e Espaços Culturais.",
        alert_type="info",
    )
    v_btn = pn.widgets.Button(name="Continuar como Visitante", button_type="default")

    def do_visitante(_):
        on_success({"id_usuario": 0, "nome": "Visitante", "email": "", "role": "Visitante"})

    v_btn.on_click(do_visitante)

    visitante_pane = pn.Column(
        pn.pane.Markdown("## Visitante"),
        v_info,
        v_btn,
        width=420
    )

    tabs = pn.Tabs(
        ("Entrar", login_pane),
        ("Cadastrar", cadastro_pane),
        ("Visitante", visitante_pane),
        dynamic=True,
    )

    return pn.Column(pn.Spacer(height=20), pn.Row(pn.Spacer(), tabs, pn.Spacer()))
