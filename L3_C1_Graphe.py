from typing import Dict, List
from itertools import product

from L3_C1_Arete import Arete


class Graphe:
    numero: int
    nombre_sommets: int
    sommets: set
    aretes: Dict[int, list]
    matrice_adjascence: List[List[bool]]
    matrice_valeurs: List[List[int]]
    djikstra_possible: bool

    def __init__(self, numero: int) -> None:
        self.numero = numero
        self.lire_fichier()
        self.initialiser_matrices()

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

        self.djikstra_possible = True

        print(f'Le graphe possède {self.nombre_sommets} sommets.')
        # Initialisation des arêtes
        for line in lines[1:]:
            # Format d'une ligne: "SommetDépart ValeurArête SommetArrivée"
            depart, valeur, arrivee = (int(i) for i in line.split(' '))

            print(f'Arête: de {depart} vers {arrivee}, de valeur {valeur}')
            arete = Arete(depart, valeur, arrivee)
            self.aretes[depart].append(arete)

            # Une arête à valeur négative signifie qu'on ne peut pas utiliser Djikstra sur le graphe
            if valeur < 0:
                self.djikstra_possible = False

    def initialiser_matrices(self) -> None:
        """
        Initialise la matrice d'adjascence, et la matrice de valeurs
        """
        self.matrice_adjascence = [[False for _ in range(self.nombre_sommets)] for __ in range(self.nombre_sommets)]
        self.matrice_valeurs = [[None for _ in range(self.nombre_sommets)] for __ in range(self.nombre_sommets)]

        for depart, aretes in self.aretes.items():
            for arete in aretes:
                self.matrice_adjascence[depart][arete.arrivee] = True
                self.matrice_valeurs[depart][arete.arrivee] = arete.valeur

        print('Adjascence:')
        for ligne in self.matrice_adjascence:
            print(' '.join(str(int(i)) for i in ligne))
        print('---')
        print('Valeurs:')
        for ligne in self.matrice_valeurs:
            for cell in ligne:
                if cell is None:
                    print(' / ', end='')
                else:
                    print("{:^3}".format(cell), end='')
            print()

    def djikstra(self, depart: int):
        pass

    def bellman(self, depart: int):
        pass
