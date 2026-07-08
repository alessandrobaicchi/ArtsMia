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
        # Recupero l'input dell'utente
        txtIdOggetto = self._view._txtIdOggetto.value

        # Verifico che l'utente non lasci il campo vuoto
        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserire un valore nel campo id",
                                                          color="red"))
            self._view.update_page()
            return

        # Verifico che l'utente inserisca un numero
        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, inserire un valore numerico nel campo id",
                                                          color="red"))
            self._view.update_page()
            return

        # Verifico che il valore inserito dall'utente sia un nodo del grafo
        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, l'id inserito non è presente nel grafo",
                                                          color="orange"))
            self._view.update_page()
            return

        # Se passo tutti i controlli stampo la componente connessa
        sizeCompConn = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contentente l'oggetto con id {idOggetto} è composta di {sizeCompConn} nodi",
                    color="green"))

        # Sblocco la funzionalità della ricerca del cammino ottimo
        self._view._ddLun.disabled = False
        self._view._btnCerca.disabled = False

        # Il dropdown ddLun deve contenere tutti i valori interi fra 2 e la lunghezza della componente connessa.
        lunValues = list(range(2, sizeCompConn))

        # Le opzioni di un dropdown devono essere degli oggetti di tipo dropdown.Option.
        # Opzione 1
        # for v in lunValues:
        #     self._view._ddLun.options.append(ft.dropdown.Option(v))

        # Opzione 2, più in stile Python
        # Uso il metodo map(). A questo metodo passo un iterable (qui una lista) e lui crea un nuovo iterable (lista).
        # Ogni elemento di questa nuova lista è l'elemento della lista vecchia a cui viene applicata una certa funzione:
        # una lambda function. In pratica, la lambda fuction per ogni elemento della lista vecchia converte
        # l'intero di lunesValues in un oggetto di tipo dropdown.Option.
        lunValuesDD = list(map(lambda x: ft.dropdown.Option(x), lunValues))

        # lunValuesDD sarà quindi una lista di oggetti di tipo dropdown.Option che posso tranquillamente assegnare
        # alle opzioni del dropdown ddLun.
        self._view._ddLun.options = lunValuesDD

        self._view.update_page()



    # Il metodo handleCerca() lo posso chiamare solo dopo aver schiacciato il pulsante "Componente connessa",
    # quindi sono sicuro di avere già l'oggetto di partenza e questo oggetto di partenza.
    def handleCerca(self,e):
        source = self._model.getNodeFromId(int(self._view._txtIdOggetto.value))
        # Posso scrivere così "fregandomene" di fare controlli, perché tutti i controlli su txtIdOggetto
        # li ho già fatti nel metodo che calcola la componente connessa (handleCompConnessa()).
        # Infatti, il metodo handleCerca() lo posso chiamare solo se ho già chiamato il pulsante di handleCompConnessa().

        lun = self._view._ddLun.value
        # Sulla variabile lun non devo fare troppi controlli perché alla fine sono numeri che ci ho messo io.
        # L'unica cosa che può succedere è che l'utente non abbia selezionato un valore nel dropdown.
        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un valore di lunghezza fra le scelte proposte",
                                                          color="red"))
            self._view.update_page()
            return

        # La variabile lun è una stringa, devo convertirla in un intero. Questo perché Flet
        # restituisce sempre stringhe per i valori dei widget.
        # Dunque, dato che self._model.getOptPath() si aspetta un intero, faccio io la conversione.
        lunInt = int(lun)

        # Ora chiamo il metodo ricorsivo.
        path, cost = self._model.getOptPath(source, lunInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un cammino che parte da {source} con un peso totale pari a {cost}.",
                    color="green"))
        self._view.txt_result.controls.append(
            ft.Text("Di seguito i nodi che compongono questo cammino:",
                    color="green"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()
