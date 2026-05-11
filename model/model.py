import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        # Definisco il grafo
        self._graph = nx.Graph()


    def buildGraph(self):
        #Aggiungo i nodi
        self._nodes = DAO.getAllNodes()
        self._graph.add_nodes_from(self._nodes)
        #Aggiungo gli archi



    def getNumNodes(self):
        return len(self._graph.nodes)


    def getNumEdges(self):
        return len(self._graph.edges)