import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        # Definisco il grafo
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        # self._idMapAO è un dizionario che associa ad ogni chiave primaria (object_id)
        # l'oggetto di tipo artObject corrispondente.
        for n in self._nodes:
            self._idMapAO[n.object_id] = n

    # ====================================== COMPONENTI CONNESSE ==============================================

    def getInfoCompConnessa(self, id_oggetto):
        # Cerco la componente connessa che contiene id_oggetto. Sfrutto networkx. Ci sono almeno 3 modi
        # per sviluppare questo metodo.

        # Devo verificare se id_oggetto è contenuto nel grafo, perché l'utente potrebbe scriverne uno a caso.
        # Inoltre, è una richiesta esplicita del testo. Faccio ciò con un metodo ad hoc: hasNode().
        # Verifico se id_oggetto è contenuto nell'idMapAO e se lo è vuol dire che è contenuto anche nel grafo.
        if not self.hasNode(id_oggetto):
            return None

        # La variabile source deve essere un nodo associato a id_oggetto: mi serve idMapAO.
        source = self._idMapAO[id_oggetto]

        # ====================================== STRATEGIA 1: dfs_tree ===========================================
        # nx.dfs_tree(G, source) costruisce l'ALBERO DI VISITA DFS.
        # È un vero grafo orientato che contiene:
        #   - tutti i nodi raggiungibili dal source
        #   - solo gli archi effettivamente usati dalla DFS
        #   - il source come radice dell'albero
        #
        # Questo albero rappresenta la COMPONENTE CONNESSA del source
        # (rispettando la direzione degli archi).
        #
        # Per questo:
        #   len(dfsTree.nodes())
        # restituisce il numero di nodi raggiungibili = dimensione della componente.
        #
        # Strategia 1 è più "pesante" perché costruisce un grafo,
        # ma è anche la più completa e intuitiva.
        #
        # Differenza con Strategia 2:
        #   - dfs_tree include il source
        #   - dfs_predecessors NO → manca sempre 1 nodo

        dfsTree = nx.dfs_tree(self._graph, source)
        # dfsTree è un albero di visita DFS, e un albero è un grafo.
        # NetworkX lo rappresenta come un grafo orientato (DiGraph)
        print("Size connesse con dfs_tree", len(dfsTree.nodes()))
        # ==========================================================================================================


        # ===================================== STRATEGIA 2: dfs_predecessors ======================================
        # nx.dfs_predecessors(G, source) restituisce un DIZIONARIO:
        #   - chiave   = nodo raggiunto dalla DFS
        #   - valore   = predecessore di quel nodo nell'albero DFS
        #
        # Quindi rappresenta implicitamente l'albero di visita DFS,
        # ma SENZA costruire un grafo (molto più leggero della strategia 1).
        #
        # Esempio struttura:
        #   { B: A, C: A, D: C, E: D }
        # Significa:
        #   - per arrivare a B sono passato da A
        #   - per arrivare a C sono passato da A
        #   - per arrivare a D sono passato da C
        #   - per arrivare a E sono passato da D
        #
        # >>> Come conto la componente connessa?
        # I "valori" del dizionario sono TUTTI i nodi raggiunti,
        # tranne il nodo sorgente (source), che NON ha predecessore.
        #
        # Quindi:
        #   len(dfsPred.values())  = numero nodi raggiunti - 1
        #
        # Per ottenere la dimensione reale della componente connessa:
        #   len(dfsPred.values()) + 1
        #
        # >>> Confronto con Strategia 1 (dfs_tree):
        #   len(dfsTree.nodes()) == len(dfsPred.values()) + 1
        #
        # >>> Nota del prof:
        # "Qui me ne mancherà uno che è il nodo source"
        #
        # In sintesi:
        # - Strategia 1 costruisce l'albero → include il source
        # - Strategia 2 usa solo i predecessori → NON include il source

        dfsPred = nx.dfs_predecessors(self._graph, source)
        print("Size connesse con dfs_predecessors", len(dfsPred.values()))
        # ========================================================================================================

        # ================================= STRATEGIA 3: node_connected_component ================================
        # Questa è la strategia CONSIGLIATA dal prof ("quella che useremo sempre").
        #
        # nx.node_connected_component(G, source) restituisce direttamente:
        #   - un SET di nodi
        #   - tutti appartenenti alla COMPONENTE CONNESSA del nodo source
        #
        # È la soluzione più semplice e più pulita:
        #   - niente alberi DFS
        #   - niente dizionari di predecessori
        #   - niente strutture intermedie
        #   - NetworkX fa tutto automaticamente
        #
        # Per ottenere la dimensione della componente:
        #   len(conn)
        #
        # conn = nx.node_connected_component(self._graph, source)
        # print("Size connessa con node_connected_component", len(conn))
        # return conn
        #
        # Vantaggi:
        #   ✔ leggibile
        #   ✔ veloce
        #   ✔ robusta
        #   ✔ include il source automaticamente

        conn = nx.node_connected_component(self._graph, source)
        # conn è un set Python che contiene tutti i nodi della componente connessa del source
        print("Size connesse con node_connected_component", len(conn))
        return len(conn)
        # ======================================================================================================




    # Questo metodo lo uso per controllare se ha senso cercare una componente connessa che
    # contiene l'id_oggetto passatogli.
    def hasNode(self, id_oggetto):
        return id_oggetto in self._idMapAO
        # La return è True se id_oggetto è contenuto nell'idMapAO e quindi è contenuto anche nel grafo.
        # La return è False altrimenti.


    def buildGraph(self):
        #Aggiungo i nodi
        self._graph.add_nodes_from(self._nodes)

        #Aggiungo gli archi
        self.addEdgesV2()

    # ---------------------------------------- Aggiunta archi (modo 1) ----------------------------------------------
    def addEdges(self):
        # Ciclo suo su tutti nodi e provo a recuperare il peso della coppia analizzata.
        # Se il peso non è None, allora aggiungo l'arco.
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgesPeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)
        # E' un metodo inefficiente dal punto di vista del tempo, ed è un classico comportamento quando si usano
        # cicli for annidati. Dunque, riscrivo in modo diverso la query nel DAO.
    # --------------------------------------------------------------------------------------------------------------
    # ---------------------------------------- Aggiunta archi (modo 2) ---------------------------------------------
    # La difficoltà di questo modo 2 è creare l'idMapAO e fare un query leggermente complicata.
    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)
    # --------------------------------------------------------------------------------------------------------------

    def getNumNodes(self):
        return len(self._graph.nodes)


    def getNumEdges(self):
        return len(self._graph.edges)