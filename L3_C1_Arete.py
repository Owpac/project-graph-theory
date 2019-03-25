class Arete:
    """
    Une simple classe, utilisée pour stocker les infos d'une arête
    """
    depart: int
    valeur: int
    arrivee: int

    def __init__(self, depart: int, valeur: int, arrivee: int):
        self.depart = depart
        self.valeur = valeur
        self.arrivee = arrivee
