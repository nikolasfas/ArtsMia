import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n
        self._bestPath = []
        self._optCost = 0

    def getOptPath(self, source, lun):
        parziale =  [source]

        # Ciclo sui vicini di source e cerco di capire se posso aggiungere i vicini, oppure no
        for n in self._graph.neighbors(source):
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                # backtracking
                parziale.pop()

        return self._optPath, self._optCost

    def _ricorsione(self, parziale, lun):
        # Condizione di terminazione
        if len(parziale) == lun:
            # verifico che questa parziale sia meglio del mio best (condizione di ottimalità),
            # ed in ogni caso esco
            if self._costoPath(parziale) > self._optCost:
                self._optCost = self._costoPath(parziale)
                self._optPath = copy.deepcopy(parziale)
            return


        # Se arrivo qui, posso ancora aggiungere nodi
        print(len(parziale))
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                # backtracking
                parziale.pop()

    def _costoPath(self, path):
        costo = 0
        for i in range(0, len(path)-1):
            costo += self._graph[path[i]][path[i+1]]["weight"]
        return costo



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

    def getNodeFromId(self, id_oggetto):
        return self._idMapAO[id_oggetto]

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