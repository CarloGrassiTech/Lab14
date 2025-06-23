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
        edges = self.getAllEdges(k)
        self.fillMapWeight(store)

        if len(nodes) != 0:
            self.grafo.add_nodes_from(nodes)
            self._nodes = nodes

        if len(edges) != 0:
            self.grafo.add_edges_from(edges)
            self._edges = edges
        else:
            print(f"il grafo ha {len(edges)} archi e {len(nodes)} nodes")

        for i in edges:
            self.grafo[i[0]][i[1]]["weight"] = self.getWeight(i[0], i[1])
        if len(self._mapWeight)!= 0:
            print(f"la mappatura per il peso ha una lunghezza di {len(self._mapWeight)}")


        print("grafo creato")

    def graphDetails(self):
        return self._nodes, self._edges

    def getAllStore(self):
        return DAO.getAllStore()

    def getAllOrders(self, store):
        return DAO.getAllOrders(store)

    def getAllEdges(self, k):
        result = []
        for v in self._nodes:
            for u in self._nodes:
                count = (u.order_date.day - v.order_date.day)
                check = 0
                if u.order_id in self._mapWeight.keys():
                    check = self._mapWeight[u.order_id]
                if (u.order_id != v.order_id and count <= int(k) and check > 0 and
                        self._mapWeight[v.order_id] > 0):
                    result.append((v, u))
        return result

    def getWeight(self, p, a):
        return self._mapWeight[p.order_id] + self._mapWeight[a.order_id]

    def fillMapWeight(self, store):
        map = DAO.getAllWeight(store)
        for i, j in map:
            self._mapWeight[i] = j