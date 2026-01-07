# src/ui/denuncias.py
import panel as pn
import pandas as pd


def view(user=None, can_edit=False, can_denunciar=False):
    pn.config.sizing_mode = "stretch_width"
    user = user or {}

    info = pn.pane.Markdown(
        f"**Usuário:** {user.get('nome', '(não informado)')}  \n"
        f"**Role:** {user.get('role', '(não informado)')}  \n"
        f"**Pode denunciar:** {'SIM' if can_denunciar else 'NÃO'}  \n"
        f"**Admin (gerenciar):** {'SIM' if can_edit else 'NÃO'}"
    )

    aviso = pn.pane.Alert(
        "Tela **Denúncias** ainda não foi implementada. Este é um placeholder.",
        alert_type="warning",
    )

    # Tabela vazia só pra manter padrão visual
    df = pd.DataFrame(columns=["id_denuncia", "data", "evento", "motivo", "descricao", "status"])
    tabela = pn.widgets.Tabulator(df, pagination="local", page_size=10)

    # Botões (apenas aparência)
    btn_criar = pn.widgets.Button(
        name="Criar denúncia (em breve)",
        button_type="primary",
        disabled=not can_denunciar,
    )

    btn_admin_status = pn.widgets.Button(
        name="Atualizar status (em breve)",
        button_type="warning",
        disabled=not can_edit,
    )

    btn_admin_excluir = pn.widgets.Button(
        name="Excluir denúncia (em breve)",
        button_type="danger",
        disabled=not can_edit,
    )

    def msg_em_breve(_):
        pn.state.notifications.warning("Funcionalidade em desenvolvimento.", duration=2500)

    btn_criar.on_click(msg_em_breve)
    btn_admin_status.on_click(msg_em_breve)
    btn_admin_excluir.on_click(msg_em_breve)

    form = pn.Card(
        pn.pane.Markdown("## Denúncias (Placeholder)"),
        info,
        aviso,
        pn.layout.Divider(),
        pn.pane.Markdown("### Ações"),
        pn.Row(btn_criar),
        pn.layout.Divider(),
        pn.pane.Markdown("### Ações administrativas"),
        pn.Row(btn_admin_status, btn_admin_excluir),
        title="Painel",
        collapsed=False,
        width=520,
    )

    dashboard = pn.Column(
        pn.Card(tabela, title="Denúncias (placeholder)", collapsed=False),
    )

    return pn.Row(form, dashboard)
