# Created by Florian on 25/03/2019


class Graphe:
    numero: int
    nombre_sommets: int
    sommets: set
    aretes: dict

    def __init__(self, numero: int) -> None:
        self.numero = numero
        self.lire_fichier()

    def lire_fichier(self) -> None:
        """
        Lit le graphe depuis un fichier.
        Initialise :
        - le nombre de sommets,
        - la liste des sommets,
        - la valeur des différentes arêtes
        """

        # Lecture du fichier
        with open(f'L3_C1_{self.numero}.txt') as f:
            lines = f.read().strip().split('\n')

        # Initialisation des sommets
        self.nombre_sommets = int(lines[0])
        self.sommets = {*range(self.nombre_sommets)}

        # On commence avec des sommets sans aucune arêtes
        self.aretes = {i: list() for i in range(self.nombre_sommets)}

        # Initialisation des arêtes
        for line in lines[1:]:
            # Format d'une ligne: "SommetDépart ValeurArête SommetArrivée"
            depart, valeur, arrivee = (int(i) for i in line.split(' '))
