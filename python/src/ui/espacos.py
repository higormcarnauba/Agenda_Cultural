import panel as pn
import matplotlib.pyplot as plt

from src.repositories import espaco_repo

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
    id_espaco = pn.widgets.IntInput(name="ID Espaço (para atualizar/excluir)", value=0, start=0)
    nome = pn.widgets.TextInput(name="Nome", placeholder="Ex: Centro Cultural...")
    rua = pn.widgets.TextInput(name="Rua", placeholder="Ex: Rua X")
    numero = pn.widgets.TextInput(name="Número", placeholder="Ex: 100")
    bairro = pn.widgets.TextInput(name="Bairro", placeholder="Ex: Centro")

    # --- Filtros ---
    filtro_nome = pn.widgets.TextInput(name="Filtro: Nome", placeholder="Parte do nome")
    filtro_bairro = pn.widgets.TextInput(name="Filtro: Bairro", placeholder="Parte do bairro")

    # --- Botões ---
    btn_consultar = pn.widgets.Button(name="Consultar (com filtro)", button_type="primary")
    btn_inserir = pn.widgets.Button(name="Inserir", button_type="success")
    btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_excluir = pn.widgets.Button(name="Excluir", button_type="danger")

    btn_grafico = pn.widgets.Button(name="Atualizar Gráfico", button_type="default")

    # --- Tabela + Gráfico ---
    tabela = pn.widgets.Tabulator(espaco_repo.listar_todos(), pagination="remote", page_size=10)
    grafico = pn.pane.Matplotlib(_bar_chart(espaco_repo.total_eventos_por_espaco(), "espaco", "total_eventos",
                                           "Total de Eventos por Espaço Cultural"),
                                 tight=True)

    def refresh_table(df=None):
        try:
            tabela.value = df if df is not None else espaco_repo.listar_todos()
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar tabela: {e}")

    def refresh_chart():
        try:
            df = espaco_repo.total_eventos_por_espaco()
            grafico.object = _bar_chart(df, "espaco", "total_eventos", "Total de Eventos por Espaço Cultural")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar gráfico: {e}")

    def on_consultar(_=None):
        try:
            df = espaco_repo.consultar(nome=filtro_nome.value_input, bairro=filtro_bairro.value_input)
            refresh_table(df)
            pn.state.notifications.success("Consulta realizada.")
        except Exception as e:
            pn.state.notifications.error(f"Erro na consulta: {e}")

    def on_inserir(_=None):
        try:
            espaco_repo.inserir(nome.value_input, rua.value_input, numero.value_input, bairro.value_input)
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Espaço inserido com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao inserir: {e}")

    def on_atualizar(_=None):
        try:
            if id_espaco.value <= 0:
                pn.state.notifications.warning("Informe o ID do espaço para atualizar.")
                return
            espaco_repo.atualizar(id_espaco.value, nome.value_input, rua.value_input, numero.value_input, bairro.value_input)
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Espaço atualizado com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar: {e}")

    def on_excluir(_=None):
        try:
            if id_espaco.value <= 0:
                pn.state.notifications.warning("Informe o ID do espaço para excluir.")
                return
            espaco_repo.excluir(id_espaco.value)
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Espaço excluído com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao excluir: {e}")

    btn_consultar.on_click(on_consultar)
    btn_inserir.on_click(on_inserir)
    btn_atualizar.on_click(on_atualizar)
    btn_excluir.on_click(on_excluir)
    btn_grafico.on_click(lambda *_: refresh_chart())

    form = pn.Card(
        pn.pane.Markdown("## Espaços Culturais (CRUD)"),
        id_espaco,
        nome, rua, numero, bairro,
        pn.layout.Divider(),
        pn.pane.Markdown("### Consulta com filtro"),
        filtro_nome, filtro_bairro,
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
