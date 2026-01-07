import panel as pn
import matplotlib.pyplot as plt

from src.repositories import artista_repo

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

    # --- Campos CRUD ---
    id_artista = pn.widgets.IntInput(name="ID Artista (para atualizar/excluir)", value=0, start=0)
    nome = pn.widgets.TextInput(name="Nome", placeholder="Nome do artista")
    cpf_rg = pn.widgets.TextInput(name="CPF/RG", placeholder="Documento (único)")
    email = pn.widgets.TextInput(name="Email", placeholder="email@...")
    numero = pn.widgets.TextInput(name="Telefone", placeholder="(DDD) ...")
    descricao = pn.widgets.TextAreaInput(name="Descrição", placeholder="Bio/descrição", height=90)

    # --- Filtros ---
    filtro_nome = pn.widgets.TextInput(name="Filtro: Nome", placeholder="Parte do nome")
    filtro_cpf = pn.widgets.TextInput(name="Filtro: CPF/RG", placeholder="Parte do doc")
    filtro_email = pn.widgets.TextInput(name="Filtro: Email", placeholder="Parte do email")

    # --- Botões ---
    btn_consultar = pn.widgets.Button(name="Consultar (com filtro)", button_type="primary")
    btn_inserir = pn.widgets.Button(name="Inserir", button_type="success")
    btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_excluir = pn.widgets.Button(name="Excluir", button_type="danger")

    top_n = pn.widgets.IntInput(name="Top N", value=10, start=1, end=50)
    btn_grafico = pn.widgets.Button(name="Atualizar Gráfico", button_type="default")

    # --- Tabela + Gráfico ---
    tabela = pn.widgets.Tabulator(artista_repo.listar_todos(), pagination="remote", page_size=10)
    df_top = artista_repo.top_artistas_por_eventos(limit=10)
    grafico = pn.pane.Matplotlib(_bar_chart(df_top, "artista", "total_eventos", "Top artistas por eventos"),
                                 tight=True)

    def refresh_table(df=None):
        try:
            tabela.value = df if df is not None else artista_repo.listar_todos()
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar tabela: {e}")

    def refresh_chart():
        try:
            df = artista_repo.top_artistas_por_eventos(limit=top_n.value)
            grafico.object = _bar_chart(df, "artista", "total_eventos", f"Top {top_n.value} artistas por eventos (agregação)")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar gráfico: {e}")

    def on_consultar(_=None):
        try:
            df = artista_repo.consultar(
                nome=filtro_nome.value_input,
                cpf_rg=filtro_cpf.value_input,
                email=filtro_email.value_input,
            )
            refresh_table(df)
            pn.state.notifications.success("Consulta realizada.")
        except Exception as e:
            pn.state.notifications.error(f"Erro na consulta: {e}")

    def on_inserir(_=None):
        try:
            artista_repo.inserir(
                nome.value_input,
                cpf_rg.value_input,
                email.value_input,
                numero.value_input,
                descricao.value_input,
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Artista inserido com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao inserir: {e}")

    def on_atualizar(_=None):
        try:
            if id_artista.value <= 0:
                pn.state.notifications.warning("Informe o ID do artista para atualizar.")
                return
            artista_repo.atualizar(
                id_artista.value,
                nome.value_input,
                cpf_rg.value_input,
                email.value_input,
                numero.value_input,
                descricao.value_input,
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Artista atualizado com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar: {e}")

    def on_excluir(_=None):
        try:
            if id_artista.value <= 0:
                pn.state.notifications.warning("Informe o ID do artista para excluir.")
                return
            artista_repo.excluir(id_artista.value)
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Artista excluído com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao excluir: {e}")

    btn_consultar.on_click(on_consultar)
    btn_inserir.on_click(on_inserir)
    btn_atualizar.on_click(on_atualizar)
    btn_excluir.on_click(on_excluir)
    btn_grafico.on_click(lambda *_: refresh_chart())

    form = pn.Card(
        pn.pane.Markdown("## Artistas "),
        id_artista,
        nome, cpf_rg, email, numero, descricao,
        pn.layout.Divider(),
        pn.pane.Markdown("### Consulta com filtro"),
        filtro_nome, filtro_cpf, filtro_email,
        pn.Row(btn_consultar),
        pn.layout.Divider(),
        pn.Row(btn_inserir, btn_atualizar, btn_excluir),
        title="Formulário",
        collapsed=False,
    )

    dashboard = pn.Column(
        pn.Card(tabela, title="Dados", collapsed=False),
        pn.Card(pn.Row(top_n, btn_grafico), grafico, title="Gráfico ", collapsed=False),
    )

    return pn.Row(form, dashboard)
