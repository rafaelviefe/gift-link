import FreeSimpleGUI as sg
from views.theme import configure_theme
from typing import Iterable


def _format_participantes(participantes: Iterable) -> list:
    """Return a list of rows for the table from Participante objects."""
    rows = []
    if not participantes:
        return rows
    for p in participantes:
        pid = p.get_id() if hasattr(p, "get_id") else ""
        username = p.get_username() if hasattr(p, "get_username") else ""
        elegivel = getattr(p, "is_elegivel", None)
        if callable(elegivel):
            eleg = "Sim" if p.is_elegivel() else "Não"
        else:
            # fallback to attribute access
            eleg = "Sim" if getattr(p, "_Participante__elegivel", False) else "Não"
        rows.append([pid, username, eleg])
    return rows


def criar_janela_cadastro(participantes: Iterable | None = None):
    """Create the participant registration window with a table showing participants.

    participantes: optional iterable of Participante objects to pre-fill the table.
    """
    configure_theme()

    headings = ["ID", "Username", "Elegível"]
    table_values = _format_participantes(participantes)

    layout = [
        [sg.Text("Cadastro de Participante", font=("Helvetica", 20, "bold"))],
        [sg.Text("Username", size=(14, 1)), sg.InputText(key="-USERNAME-")],
        [
            sg.Table(
                values=table_values,
                headings=headings,
                auto_size_columns=False,
                col_widths=[8, 30, 12],
                justification="center",
                num_rows=10,
                key="-TABLE-",
                enable_events=False,
                alternating_row_color=None,
            )
        ],
        [sg.Button("Cadastrar", key="-SUBMIT-"), sg.Button("Voltar", key="-VOLTAR-")],
    ]

    return sg.Window(
        "Cadastro - GiftLink", layout, finalize=True, element_justification="center"
    )


def atualizar_tabela(window, participantes: Iterable | None):
    """Update the table in the given window with the provided participantes list."""
    if window is None:
        return
    rows = _format_participantes(participantes)
    try:
        window["-TABLE-"].update(values=rows)
    except Exception:
        # in case the element/key doesn't exist, ignore silently
        pass
