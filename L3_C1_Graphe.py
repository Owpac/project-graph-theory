from typing import Dict, List
from L3_C1_Arete import Arete


class Graphe:
    numero: int
    nombre_sommets: int
    sommets: set
    aretes: Dict[int, list]
    matrice_adjascence: List[List[bool]]

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

        print(f'Le graphe possède {self.nombre_sommets} sommets.')
        # Initialisation des arêtes
        for line in lines[1:]:
            # Format d'une ligne: "SommetDépart ValeurArête SommetArrivée"
            depart, valeur, arrivee = (int(i) for i in line.split(' '))

            print(f'Arête: de {depart} vers {arrivee}, de valeur {valeur}')
            arete = Arete(depart, valeur, arrivee)
            self.aretes[depart].append(arete)

    def initialiser_matrice_adjascence(self):
        pass
