import copy

import networkx as nx
from networkx.classes import edges

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self._edges = []
        self._nodes = []
        self._idMap = {}
        self._mapWeight = {}

    def build_graph(self, store, k):
        nodes = self.getAllOrders(store)
        if len(nodes) != 0:
            self._nodes = nodes
        for i in nodes:
            self._idMap[i.order_id] = i
        self.fillMapWeight(store)
        edges = self.getAllEdges(k)


        if len(nodes) != 0:
            self.grafo.add_nodes_from(nodes)
            self._nodes = nodes

        if len(edges) != 0:
            self.grafo.add_edges_from(edges)
            self._edges = edges
        else:
            print(f"il grafo ha {len(edges)} archi e {len(nodes)} nodes")

        for i in edges:
            peso = int(self.getWeight(i[0], i[1]))
            if peso > 0:
                self.grafo[i[0]][i[1]]["weight"] = peso
        if len(self._mapWeight)!= 0:
            print(f"la mappatura per il peso ha una lunghezza di {len(self._mapWeight)}")
        print("grafo creato")

    def graphDetails(self):
        return self._nodes, self._edges

    def getAllStore(self):
        return DAO.getAllStore()

    def getAllOrders(self, store):
        return DAO.getAllOrders(store)

    def getAllEdgesProblem(self, k):
        result = []
        for v in self._nodes:
            for u in self._nodes:
                count = (u.order_date - v.order_date).days
                check = 0
                if u.order_id in self._mapWeight.keys():
                    check = int(self._mapWeight[u.order_id])
                if (int(u.order_id) != int(v.order_id) and count <= int(k) and check > 0 and
                        self._mapWeight[v.order_id] > 0):
                    result.append((v, u))
        return result

    def getAllEdges(self, k):
        result = []
        for v in self._nodes:
            for u in self._nodes:
                if v.order_id == u.order_id:
                    continue  # salta stesso ordine

                delta_days = (u.order_date - v.order_date).days

                # Vogliamo solo ordini in avanti nel tempo, fino a k giorni
                if 0 < delta_days <= int(k):
                    weight_v = self._mapWeight.get(v.order_id, 0)
                    weight_u = self._mapWeight.get(u.order_id, 0)
                    if weight_v > 0 and weight_u > 0:
                        result.append((v, u))  # arco da v a u
        return result

    def getWeight(self, p, a):
        return self._mapWeight[p.order_id] + self._mapWeight[a.order_id]

    def getWeight1(self, p, a):
        return self._mapWeight.get(p.order_id, 0) + self._mapWeight.get(a.order_id, 0)

    def fillMapWeight(self, store):
        map = DAO.getAllWeight(store)
        for i, j in map:
            self._mapWeight[i] = j

    def calcolaMaxPath(self, source):
        path = nx.DiGraph()

        path =  copy.deepcopy(nx.dag_longest_path(self.grafo), )
        print(path.nodes)
        print(path.edges)
        return path

    def getLongestPathFrom(self, source):
        if not nx.is_directed_acyclic_graph(self.grafo):
            print("Errore: il grafo contiene cicli, impossibile calcolare il percorso più lungo da una sorgente.")
            return [], 0

        # Calcola tutte le distanze massime dal nodo sorgente usando topological sort
        dist = {node: float('-inf') for node in self.grafo.nodes}
        dist[source] = 0
        pred = {node: None for node in self.grafo.nodes}

        for node in nx.topological_sort(self.grafo):
            for succ in self.grafo.successors(node):
                weight = self.grafo[node][succ].get("weight", 1)
                if dist[node] + weight > dist[succ]:
                    dist[succ] = dist[node] + weight
                    pred[succ] = node

        # Trova il nodo di arrivo con distanza massima
        end_node = max(dist, key=dist.get)
        if dist[end_node] == float('-inf'):
            print("Nessun percorso valido dal nodo sorgente.")
            return [], 0

        # Ricostruisci il percorso
        path = []
        current = end_node
        while current is not None:
            path.insert(0, current)
            current = pred[current]

        print("Percorso più lungo da sorgente:", [o.order_id for o in path])
        print("Lunghezza totale (peso):", dist[end_node])
        return path, dist[end_node]
