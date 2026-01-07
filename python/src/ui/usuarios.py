# src/ui/usuarios.py
import panel as pn
import matplotlib.pyplot as plt

# Import direto (evita problemas de circular import)
import src.repositories.usuario_repo as usuario_repo


def _bar_chart(df, x_col, y_col, title):
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(111)

    if df is None or df.empty:
        ax.set_title(title)
        ax.text(0.5, 0.5, "Sem dados", ha="center", va="center")
        ax.set_axis_off()
        return fig

    x = df[x_col].astype(str).tolist()
    y = df[y_col].tolist()
    ax.bar(x, y)
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


def view():
    pn.config.sizing_mode = "stretch_width"

    # --- Papéis (role) para dropdown ---
    df_roles = usuario_repo.listar_roles()

    # Se não tiver papel cadastrado, evita quebrar a tela
    if df_roles is None or df_roles.empty:
        role_options = {"(sem papéis cadastrados)": 0}
        role_filter_options = [""]
    else:
        # listar_roles retorna id_papel com alias id_role (pra UI ficar simples)
        role_options = {row["nome"]: int(row["id_role"]) for _, row in df_roles.iterrows()}
        role_filter_options = [""] + list(role_options.keys())

    # --- Campos CRUD ---
    id_usuario = pn.widgets.IntInput(name="ID Usuário (para atualizar/excluir)", value=0, start=0)
    nome = pn.widgets.TextInput(name="Nome", placeholder="Nome do usuário")
    email = pn.widgets.TextInput(name="Email", placeholder="email@...")
    cpf_rg = pn.widgets.TextInput(name="CPF/RG", placeholder="Documento (único)")
    senha_hash = pn.widgets.PasswordInput(name="Senha (hash/placeholder)", placeholder="para protótipo pode ser texto")

    # Aqui o valor é o id_papel no banco (mas vem como id_role por alias do repo)
    papel = pn.widgets.Select(name="Papel (FK - id_papel)", options=role_options)

    # --- Filtros ---
    filtro_nome = pn.widgets.TextInput(name="Filtro: Nome", placeholder="Parte do nome")
    filtro_email = pn.widgets.TextInput(name="Filtro: Email", placeholder="Parte do email")
    filtro_papel = pn.widgets.Select(name="Filtro: Papel", options=role_filter_options, value="")

    # --- Botões ---
    btn_consultar = pn.widgets.Button(name="Consultar (com filtro)", button_type="primary")
    btn_inserir = pn.widgets.Button(name="Inserir", button_type="success")
    btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_excluir = pn.widgets.Button(name="Excluir", button_type="danger")
    btn_grafico = pn.widgets.Button(name="Atualizar Gráfico", button_type="default")

    # --- Tabela + Gráfico ---
    tabela = pn.widgets.Tabulator(usuario_repo.listar_todos(), pagination="remote", page_size=10)
    grafico = pn.pane.Matplotlib(
        _bar_chart(usuario_repo.usuarios_por_role(), "role", "total", "Usuários por papel"),
        tight=True
    )

    def refresh_table(df=None):
        try:
            tabela.value = df if df is not None else usuario_repo.listar_todos()
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar tabela: {e}")

    def refresh_chart():
        try:
            df = usuario_repo.usuarios_por_role()
            grafico.object = _bar_chart(df, "role", "total", "Usuários por papel (agregação)")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar gráfico: {e}")

    def on_consultar(_=None):
        try:
            df = usuario_repo.consultar(
                nome=filtro_nome.value_input,
                email=filtro_email.value_input,
                role_nome=filtro_papel.value,
            )
            refresh_table(df)
            pn.state.notifications.success("Consulta realizada.")
        except Exception as e:
            pn.state.notifications.error(f"Erro na consulta: {e}")

    def on_inserir(_=None):
        try:
            if papel.value == 0:
                pn.state.notifications.warning("Cadastre papéis na tabela 'role' antes de inserir usuários.")
                return

            usuario_repo.inserir(
                nome.value_input,
                email.value_input,
                cpf_rg.value_input,
                senha_hash.value_input,
                papel.value,  # <- id_papel (via alias do repo)
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Usuário inserido com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao inserir: {e}")

    def on_atualizar(_=None):
        try:
            if id_usuario.value <= 0:
                pn.state.notifications.warning("Informe o ID do usuário para atualizar.")
                return

            if papel.value == 0:
                pn.state.notifications.warning("Selecione um papel válido.")
                return

            usuario_repo.atualizar(
                id_usuario.value,
                nome.value_input,
                email.value_input,
                cpf_rg.value_input,
                senha_hash.value_input,
                papel.value,  # <- id_papel
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Usuário atualizado com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar: {e}")

    def on_excluir(_=None):
        try:
            if id_usuario.value <= 0:
                pn.state.notifications.warning("Informe o ID do usuário para excluir.")
                return
            usuario_repo.excluir(id_usuario.value)
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Usuário excluído com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao excluir: {e}")

    btn_consultar.on_click(on_consultar)
    btn_inserir.on_click(on_inserir)
    btn_atualizar.on_click(on_atualizar)
    btn_excluir.on_click(on_excluir)
    btn_grafico.on_click(lambda *_: refresh_chart())

    form = pn.Card(
        pn.pane.Markdown("## Usuários (CRUD)"),
        id_usuario,
        nome, email, cpf_rg, senha_hash, papel,
        pn.layout.Divider(),
        pn.pane.Markdown("### Consulta com filtro"),
        filtro_nome, filtro_email, filtro_papel,
        pn.Row(btn_consultar),
        pn.layout.Divider(),
        pn.Row(btn_inserir, btn_atualizar, btn_excluir),
        title="Formulário",
        collapsed=False,
    )

    dashboard = pn.Column(
        pn.Card(tabela, title="Dados", collapsed=False),
        pn.Card(pn.Row(btn_grafico), grafico, title="Gráfico (agregação)", collapsed=False),
    )

    return pn.Row(form, dashboard)

