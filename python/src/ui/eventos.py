import panel as pn
import matplotlib.pyplot as plt

from src.repositories import evento_repo, espaco_repo

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

    # --- Carrega espaços para dropdown ---
    df_esp = espaco_repo.listar_para_select()
    espaco_options = {f"{row['nome']} (ID {row['id_espaco_cult']})": int(row["id_espaco_cult"]) for _, row in df_esp.iterrows()}
    if not espaco_options:
        espaco_options = {"(Cadastre um espaço primeiro)": None}

    # --- Campos CRUD ---
    id_evento = pn.widgets.IntInput(name="ID Evento ", value=0, start=0)
    titulo = pn.widgets.TextInput(name="Título", placeholder="Ex: Show ...")
    descricao = pn.widgets.TextAreaInput(name="Descrição", placeholder="Detalhes do evento", height=90)
    categoria = pn.widgets.TextInput(name="Categoria", placeholder="Ex: Música / Feira / Teatro")
    capacidade = pn.widgets.IntInput(name="Capacidade", value=0, start=0)
    data_inicio = pn.widgets.DatetimePicker(name="Data Início")
    data_fim = pn.widgets.DatetimePicker(name="Data Fim")
    preco = pn.widgets.FloatInput(name="Preço", value=0.0, start=0.0)
    status = pn.widgets.Select(name="Status", options=["ATIVO", "CANCELADO", "ENCERRADO"], value="ATIVO")
    espaco = pn.widgets.Select(name="Espaço Cultural (FK)", options=espaco_options)

    # --- Filtros ---
    filtro_titulo = pn.widgets.TextInput(name="Filtro: Título", placeholder="Parte do título")
    filtro_categoria = pn.widgets.TextInput(name="Filtro: Categoria", placeholder="Parte da categoria")
    filtro_status = pn.widgets.Select(name="Filtro: Status", options=["", "ATIVO", "CANCELADO", "ENCERRADO"], value="")
    filtro_espaco = pn.widgets.Select(name="Filtro: Espaço", options={"Todos": None, **espaco_options}, value=None)
    filtro_data_de = pn.widgets.DatePicker(name="Data início (de)")
    filtro_data_ate = pn.widgets.DatePicker(name="Data início (até)")

    # --- Botões ---
    btn_consultar = pn.widgets.Button(name="Consultar (com filtro)", button_type="primary")
    btn_inserir = pn.widgets.Button(name="Inserir", button_type="success")
    btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="warning")
    btn_excluir = pn.widgets.Button(name="Excluir", button_type="danger")

    grafico_tipo = pn.widgets.RadioButtonGroup(
        name="Gráfico",
        options=["Por mês", "Por categoria"],
        value="Por mês"
    )
    btn_grafico = pn.widgets.Button(name="Atualizar Gráfico", button_type="default")

    # --- Tabela + Gráfico ---
    tabela = pn.widgets.Tabulator(evento_repo.listar_todos(), pagination="remote", page_size=10)
    grafico = pn.pane.Matplotlib(_bar_chart(evento_repo.eventos_por_mes(), "mes", "total", "Eventos por mês"),
                                 tight=True)

    def refresh_table(df=None):
        try:
            tabela.value = df if df is not None else evento_repo.listar_todos()
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar tabela: {e}")

    def refresh_chart():
        try:
            if grafico_tipo.value == "Por mês":
                df = evento_repo.eventos_por_mes()
                grafico.object = _bar_chart(df, "mes", "total", "Eventos por mês")
            else:
                df = evento_repo.eventos_por_categoria()
                grafico.object = _bar_chart(df, "categoria", "total", "Eventos por categoria ")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar gráfico: {e}")

    def on_consultar(_=None):
        try:
            df = evento_repo.consultar(
                titulo=filtro_titulo.value_input,
                categoria=filtro_categoria.value_input,
                status=filtro_status.value,
                id_espaco_cult=filtro_espaco.value,
                data_inicio_de=str(filtro_data_de.value) if filtro_data_de.value else "",
                data_inicio_ate=str(filtro_data_ate.value) if filtro_data_ate.value else "",
            )
            refresh_table(df)
            pn.state.notifications.success("Consulta realizada.")
        except Exception as e:
            pn.state.notifications.error(f"Erro na consulta: {e}")

    def on_inserir(_=None):
        try:
            if espaco.value is None:
                pn.state.notifications.warning("Selecione um Espaço Cultural válido.")
                return
            evento_repo.inserir(
                titulo.value_input,
                descricao.value_input,
                categoria.value_input,
                capacidade.value,
                data_inicio.value,
                data_fim.value,
                preco.value,
                status.value,
                espaco.value,
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Evento inserido com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao inserir: {e}")

    def on_atualizar(_=None):
        try:
            if id_evento.value <= 0:
                pn.state.notifications.warning("Informe o ID do evento para atualizar.")
                return
            if espaco.value is None:
                pn.state.notifications.warning("Selecione um Espaço Cultural válido.")
                return
            evento_repo.atualizar(
                id_evento.value,
                titulo.value_input,
                descricao.value_input,
                categoria.value_input,
                capacidade.value,
                data_inicio.value,
                data_fim.value,
                preco.value,
                status.value,
                espaco.value,
            )
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Evento atualizado com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao atualizar: {e}")

    def on_excluir(_=None):
        try:
            if id_evento.value <= 0:
                pn.state.notifications.warning("Informe o ID do evento para excluir.")
                return
            evento_repo.excluir(id_evento.value)
            refresh_table()
            refresh_chart()
            pn.state.notifications.success("Evento excluído com sucesso!")
        except Exception as e:
            pn.state.notifications.error(f"Erro ao excluir: {e}")

    btn_consultar.on_click(on_consultar)
    btn_inserir.on_click(on_inserir)
    btn_atualizar.on_click(on_atualizar)
    btn_excluir.on_click(on_excluir)
    btn_grafico.on_click(lambda *_: refresh_chart())

    form = pn.Card(
        pn.pane.Markdown("## Eventos "),
        id_evento,
        titulo, descricao, categoria, capacidade,
        pn.Row(data_inicio, data_fim),
        pn.Row(preco, status),
        espaco,
        pn.layout.Divider(),
        pn.pane.Markdown("### Consulta com filtro"),
        filtro_titulo, filtro_categoria,
        pn.Row(filtro_status, filtro_espaco),
        pn.Row(filtro_data_de, filtro_data_ate),
        pn.Row(btn_consultar),
        pn.layout.Divider(),
        pn.Row(btn_inserir, btn_atualizar, btn_excluir),
        title="Formulário",
        collapsed=False,
    )

    dashboard = pn.Column(
        pn.Card(tabela, title="Dados", collapsed=False),
        pn.Card(pn.Row(grafico_tipo, btn_grafico), grafico, title="Gráfico (agregação)", collapsed=False),
    )

    return pn.Row(form, dashboard)
