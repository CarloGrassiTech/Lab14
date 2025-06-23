import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceStore=None

    def fillDD(self):
        stores = self._model.getAllStore()
        if(len(stores) == 0):
            print("No stores found")
            return
        for i in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(data=i, text=i.store_id))
        self._view.update_page()

    def handleDD(self, e):
        print(e.data)
        if self._view._ddStore.value != None:
            self._choiceStore = self._view._ddStore.value

    def handleCreaGrafo(self, e):
        store = self._choiceStore
        k = self._view._txtIntK.value
        if self._choiceStore == None or k is not int:
            self._view.controls.clear()
            self._view.controls.append(ft.Text("Selezionare uno store, e un numero di giorni valido"))
            self._view.update_page()
        self._model.build_graph(store, k)
        nodi, archi = self._model.graphDetails()
        dd_nodes = []
        for i in self._model._nodes:
            dd_nodes.append(ft.dropdown.Option(data=i, text=i.order_id))
        self._view._ddNode.options = dd_nodes
        self._view.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"il grafo è stato creato correttamente con {len(nodi)} nodi e {len(archi)} archi"))
        self._view.update_page()

    def handleCerca(self, e):
        ddGiven = self._view._ddNode.value
        if ddGiven == None:
            self._view.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"selezionare un nodo valido nel dropdown"))
            self._view.update_page()
            return
        path = self._model.calcolaMaxPath(ddGiven)
        self._view.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"il cammino più lungo partendo dal nodo {ddGiven} è di : {len(path)}"))
        self._view.update_page()
        pass

    def handleRicorsione(self, e):
        pass
