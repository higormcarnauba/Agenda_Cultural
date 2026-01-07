# src/ui/denuncias.py
import panel as pn
import matplotlib.pyplot as plt

# Import direto (evita circular import e não depende do __init__.py)
import src.repositories.denuncia_repo as denuncia_repo
import src.repositories.usuario_repo as usuario_repo
import src.repositories.evento_repo as evento_repo


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

    # --- Dropdowns (usuários e eventos) ---
    df_users = usuario_repo.listar_todos()
    user_options = {
        f"{row['nome']} (ID {row['id_usuario']})": int(row["id_usuario"])
        for _, row in df_users.iterrows()
    }
    if not user_options:
        user_options = {"(Cadastre usuário primeiro)": None}

    df_events = evento_repo.listar_todos()
    event_options = {
        f"{row['titulo']} (ID {row['id_evento']})": int(row["id_evento"])
        for _, row in df_events.iterrows()
    }
    if not event_options:
        event_options = {"(Cadastre evento primeiro)": None}

    # --- Campos CRUD ---
    id_denuncia = pn.widgets.IntInput(name="ID Denúncia (para atualizar/excluir)", value=0, start=0)
    id_usuario = pn.widgets.Select(name="Usuário (FK)", options=user_options)
    id_evento = pn.widgets.Select(name="Evento (FK)", options=event_options)
    motivo = pn.widgets.TextInput(name="Motivo", placeholder="Ex: Som muito alto")
    descricao = pn.widgets.TextAreaInput(name="Descrição", placeholder="Detalhes", height=90)
    status = pn.widgets.Select(name="Status", options=["ABERTA", "EM_ANALISE", "RESOLVIDA"], value="ABERTA")

    # --- Filtros ---
    filtro_status = pn.widgets.Select(
        name="Filtro: Status",
        options=["", "ABERTA", "EM_ANALISE", "RESOLVIDA"],
        value=""
    )
    filtro_motivo = pn.widgets.TextInput(name="Filtro: Motivo", placeholder="Parte do motivo")
    filtro_data_de = pn.widgets.DatePicker(name="Data (de)")
    filtro_data_ate = pn.widgets.DatePicker(name="Data (até)")

    # --- Botões ---
    btn_consultar = pn.widgets.Button(name="Consultar (com filtro)", button_type="primary")
    btn_inserir = pn.widgets.Button(name="Inserir", button_type="success")
    btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_excluir = pn.widgets.Button(name="Excluir", button_type="danger")
    btn_grafico = pn.widgets.Button(name="Atualizar Gráfico", button_type="default")

    # --- Tabela + Gráfico ---
    tabela = pn.widgets.Tabulator(denuncia_repo.listar_todos(), pagination="remote", page_size=10)
    grafico = pn.pane.Matplotlib(
        _bar_chart(denuncia_repo.denuncias_por_status(), "status", "total", "Denúncias por status"),
        tight=True
    )

    def refresh_table(df=None):
        try:
            tabela.value = df if df is not None else denuncia_repo.listar_todos()
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar tabela: {e}")

    def refresh_chart():
        try:
            df = denuncia_repo.denuncias_por_status()
            grafico.object = _bar_chart(df, "status", "total", "Denúncias por status (agregação)")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar gráfico: {e}")

    def on_consultar(_=None):
        try:
            df = denuncia_repo.consultar(
                status=filtro_status.value,
                motivo=filtro_motivo.value_input,
                data_de=str(filtro_data_de.value) if filtro_data_de.value else "",
                data_ate=str(filtro_data_ate.value) if filtro_data_ate.value else "",
            )
            refresh_table(df)
            pn.state.notifications.success("Consulta realizada.")
        except Exception as e:
            pn.state.notifications.error(f"Erro na consulta: {e}")

    def on_inserir(_=None):
        try:
            if id_usuario.value is None or id_evento.value is None:
                pn.state.notifications.warning("Selecione um usuário e um evento válidos.")
                return
            denuncia_repo.inserir(
                id_usuario.value,
                id_evento.value,
                motivo.value_input,
                descricao.value_input,
                status.value,
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Denúncia inserida com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao inserir: {e}")

    def on_atualizar(_=None):
        try:
            if id_denuncia.value <= 0:
                pn.state.notifications.warning("Informe o ID da denúncia para atualizar.")
                return
            if id_usuario.value is None or id_evento.value is None:
                pn.state.notifications.warning("Selecione um usuário e um evento válidos.")
                return
            denuncia_repo.atualizar(
                id_denuncia.value,
                id_usuario.value,
                id_evento.value,
                motivo.value_input,
                descricao.value_input,
                status.value,
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Denúncia atualizada com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar: {e}")

    def on_excluir(_=None):
        try:
            if id_denuncia.value <= 0:
                pn.state.notifications.warning("Informe o ID da denúncia para excluir.")
                return
            denuncia_repo.excluir(id_denuncia.value)
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Denúncia excluída com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao excluir: {e}")

    btn_consultar.on_click(on_consultar)
    btn_inserir.on_click(on_inserir)
    btn_atualizar.on_click(on_atualizar)
    btn_excluir.on_click(on_excluir)
    btn_grafico.on_click(lambda *_: refresh_chart())

    form = pn.Card(
        pn.pane.Markdown("## Denúncias (CRUD)"),
        id_denuncia,
        id_usuario, id_evento,
        motivo, descricao, status,
        pn.layout.Divider(),
        pn.pane.Markdown("### Consulta com filtro"),
        filtro_status, filtro_motivo,
        pn.Row(filtro_data_de, filtro_data_ate),
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
