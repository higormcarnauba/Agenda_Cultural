import panel as pn
import pandas as pd

def view(user=None, can_edit=False, can_denunciar=False):
    user = user or {}
    df = pd.DataFrame(columns=["id_evento", "titulo", "data", "local", "status"])

    tabela = pn.widgets.Tabulator(df, pagination="local", page_size=10)

    btn_consultar = pn.widgets.Button(name="Consultar", button_type="primary")
    btn_inserir   = pn.widgets.Button(name="Inserir", button_type="success", disabled=not can_edit)
    btn_atualizar = pn.widgets.Button(name="Atualizar", button_type="warning", disabled=not can_edit)
    btn_excluir   = pn.widgets.Button(name="Excluir", button_type="danger", disabled=not can_edit)

    aviso = pn.pane.Alert(
        "Tela **Eventos** ainda não foi implementada. Este é um placeholder.",
        alert_type="warning",
    )

    info = pn.pane.Markdown(
        f"**Usuário:** {user.get('nome', '(não informado)')}  \n"
        f"**Role:** {user.get('role', '(não informado)')}  \n"
        f"**Edição:** {'SIM' if can_edit else 'NÃO'}"
    )

    return pn.Row(
        pn.Card(
            pn.pane.Markdown("## Eventos"),
            info,
            aviso,
            pn.Row(btn_consultar, btn_inserir, btn_atualizar, btn_excluir),
            title="Ações",
            collapsed=False,
        ),
        pn.Card(tabela, title="Tabela (placeholder)", collapsed=False),
    )
