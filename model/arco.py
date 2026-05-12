from dataclasses import dataclass

from model.artObject import ArtObject


@dataclass
class Arco:
    o1: ArtObject
    o2: ArtObject
    peso: int


# NOTA. Qui non mi serve definire __hash__ e __eq__ perché non confronterò mai due archi
# e non li metterò come chiavi nel dizionario.
# Creo questa classe solo per rappresentare l'output della query in getAllEdges() nel DAO.