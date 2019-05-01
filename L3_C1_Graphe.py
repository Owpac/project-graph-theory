from typing import Dict, List, Set, Optional

from L3_C1_Bellman import BellmanSolveur
from L3_C1_Djikstra import DjikstraResolveur
from L3_C1_Arete import Arete

from L3_C1_affichage_graphe import affichage_matrice


class Graphe:
    numero: int
    nombre_sommets: int
    sommets: Set[int]
    liste_sommets: List[int]
    aretes: Dict[int, list]
    matrice_adjascence: List[List[bool]]
    matrice_valeurs: List[List[Optional[int]]]
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

        self.liste_sommets = list(range(self.nombre_sommets))
        self.sommets = {*self.liste_sommets}

        # On commence avec des sommets sans aucune arêtes
        self.aretes = {i: list() for i in range(self.nombre_sommets)}

        self.djikstra_possible = True

        # Initialisation des arêtes
        for line in lines[1:]:
            # Format d'une ligne: "SommetDépart ValeurArête SommetArrivée"
            depart, valeur, arrivee = (int(i) for i in line.split(' '))

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

    def afficher(self):
        print(f'Le graphe possède {self.nombre_sommets} sommets.')

        for depart, aretes in self.aretes.items():
            print(f'Arêtes au départ de {depart}:')
            for arete in aretes:
                print(f'\t-> Arête vers {arete.arrivee}, de valeur {arete.valeur}')

        print("\nMatrice d'adjascence:")
        affichage_matrice(self.matrice_adjascence, self.liste_sommets, self.liste_sommets, {False: '0', True: '1'})

        print('\nMatrice de valeurs:')
        affichage_matrice(self.matrice_valeurs, self.liste_sommets, self.liste_sommets, {None: ''})
        print()


    def djikstra(self, depart: int):
        resolveur = DjikstraResolveur(self.matrice_valeurs, self.liste_sommets)
        resolveur.resoudre(depart)
        print("Déroulement de l'algorithme :")
        resolveur.afficher_tableau()

        print('Résultat :')
        resolveur.afficher_resultat()


    def bellman(self, depart: int):
        solveur = BellmanSolveur(self.matrice_valeurs, self.liste_sommets)
        solveur.resoudre(depart)