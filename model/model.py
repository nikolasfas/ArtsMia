import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n

    def getInfoCompConnessa(self, id_oggetto):
        # CERCARE COMPONENETE CONNESSA CHE CONTIENE id_oggetto
        if not self.hasNode(id_oggetto):
            return None
        source = self._idMapAO[id_oggetto]

        # 1. FARE UNA RICERCA DFS E CONTARE I NUOVI NODI DELL'ALBERO
        dfsTree = nx.dfs_tree(self._graph, source)
        print(f"size connessa con dfs_tree {len(dfsTree)}")

        # 2.
        dfsPrede = nx.dfs_predecessors(self._graph, source)
        print(f"size connessa con dfs_predecessors {len(dfsPrede.values())}")

        # 3. UTILIZZARE METODI APPOSITI LIBRERIA
        conn = nx.node_connected_component(self._graph, source)
        print(f"size connessa con node_connected_component {len(conn)}")
        return len(conn)


    def hasNode(self, id_oggetto):
        return id_oggetto in self._idMapAO

    def buildGraph(self):
        # AGGIUNGE I NODI
        self._graph.add_nodes_from(self._nodes)
        # AGGIUNGE GLI ARCHI
        self.addEdgesV2()

    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight = peso)
                    #print(f"Aggiunto arco fra {u} e {v} con peso {peso}")

    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight = e.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)