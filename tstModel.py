from model.model import Model

# ------------------------------------------- Modello di test(extra) ----------------------------------------------

mdl = Model()
mdl.buildGraph()
print(f"Il grafo creato contiene {mdl.getNumNodes()} nodi e "
      f"{mdl.getNumEdges()} archi!")