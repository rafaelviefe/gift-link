import FreeSimpleGUI as sg
from views.theme import configure_theme
from typing import List, Optional
from controller.item_controller import ItemController
from model.participante import Participante
from model.item import Item

class TelaListaDesejos:
    def __init__(self, item_controller: ItemController, participante: Participante):
        configure_theme()
        self.__item_controller = item_controller
        self.__participante = participante
        self.__itens: List[Item] = []
        self.__janela = None

    def _format_itens(self) -> list:
        rows = []
        self.__itens, _ = self.__item_controller.listar_por_participante(
            self.__participante
        )
        if not self.__itens:
            return rows
        for item in self.__itens:
            rows.append(
                [
                    item.get_id(),
                    item.get_nome(),
                    f"R$ {item.get_preco():.2f}",
                ]
            )
        return rows

    def __criar_janela(self):
        headings = ["ID", "Nome", "Preço Sugerido"]
        table_values = self._format_itens()

        layout_tabela = [
            [
                sg.Table(
                    values=table_values,
                    headings=headings,
                    auto_size_columns=False,
                    col_widths=[8, 30, 15],
                    justification="center",
                    num_rows=10,
                    key="-TABLE-",
                    enable_events=True,
                )
            ],
            [sg.Button("Remover Item Selecionado", key="-REMOVER-", disabled=True)],
        ]

        layout_cadastro = [
            [
                sg.Text("Nome:", size=(10, 1)),
                sg.InputText(key="-NOME-", size=(35, 1)),
            ],
            [
                sg.Text("Preço (R$):", size=(10, 1)),
                sg.InputText(key="-PRECO-", size=(15, 1)),
            ],
            [sg.Button("Adicionar Item", key="-SUBMIT_CADASTRO-")],
        ]

        layout = [
            [sg.Text("Minha Lista de Desejos", font=("Helvetica", 20, "bold"))],
            [sg.Frame("Meus Itens", layout_tabela)],
            [sg.Frame("Adicionar Novo Item", layout_cadastro)],
            [sg.Button("Voltar", key="-VOLTAR-")],
        ]
        return sg.Window(
            "Lista de Desejos - GiftLink",
            layout,
            finalize=True,
            element_justification="center",
        )

    def __atualizar_tabela(self):
        if not self.__janela:
            return
        rows = self._format_itens()
        self.__janela["-TABLE-"].update(values=rows)
        self.__janela["-REMOVER-"].update(disabled=True)

    def __limpar_campos_cadastro(self):
        self.__janela["-NOME-"].update("")
        self.__janela["-PRECO-"].update("")

    def __obter_item_selecionado(self, valores) -> Optional[Item]:
        try:
            indices_selecionados = valores["-TABLE-"]
            if not indices_selecionados:
                return None

            indice_item = indices_selecionados[0]
            item_selecionado = self.__itens[indice_item]
            return item_selecionado
        except Exception:
            return None

    def abrir(self):
        self.__janela = self.__criar_janela()
        item_selecionado = None

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == "-VOLTAR-":
                self.fechar()
                return "painel_participante", self.__participante, None

            if evento == "-SUBMIT_CADASTRO-":
                nome = valores["-NOME-"]
                preco_str = valores["-PRECO-"]

                _, mensagem = self.__item_controller.registrar(
                    nome, preco_str, self.__participante
                )
                sg.popup(mensagem)
                self.__limpar_campos_cadastro()
                self.__atualizar_tabela()

            if evento == "-TABLE-":
                item_selecionado = self.__obter_item_selecionado(valores)
                if item_selecionado:
                    self.__janela["-REMOVER-"].update(disabled=False)
                else:
                    self.__janela["-REMOVER-"].update(disabled=True)

            if evento == "-REMOVER-":
                if item_selecionado:
                    confirm = sg.popup_yes_no(
                        f"Tem certeza que deseja remover o item '{item_selecionado.get_nome()}'?"
                    )
                    if confirm == "Yes":
                        item_id = item_selecionado.get_id()
                        sucesso, msg = self.__item_controller.remover(item_id)
                        sg.popup(msg)
                        if sucesso:
                            self.__atualizar_tabela()
                
                item_selecionado = None
                self.__janela["-REMOVER-"].update(disabled=True)


    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None