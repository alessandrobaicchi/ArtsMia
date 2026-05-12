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