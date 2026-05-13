from model.model import Model

# ------------------------------------------- Modello di test(extra) ----------------------------------------------

mdl = Model()
mdl.buildGraph()
print(f"Il grafo creato contiene {mdl.getNumNodes()} nodi e "
      f"{mdl.getNumEdges()} archi!")

mdl.getInfoCompConnessa(1224)
# 1224 è un source preso dal DB