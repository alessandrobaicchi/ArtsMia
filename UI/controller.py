import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleAnalizzaOggetti(self,e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi"
                                                      f" e {self._model.getNumEdges()} archi!"))
        # Dopo aver eseguito questo metodo rendo usabili dall'utente i due componenti grafici che seguono, che
        # nel View ho volutamente disabilitato (in fase di creazione dell'interfaccia (load_interface()))
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False

        self._view.update_page()



    def handleCompConnessa(self,e):
        pass

