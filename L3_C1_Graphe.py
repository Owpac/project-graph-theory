from typing import Dict, List, Set, Optional

from L3_C1_Bellman import BellmanSolveur
from L3_C1_Dijkstra import DijkstraResolveur
from L3_C1_Arete import Arete

from L3_C1_affichage import affichage_matrice


class Graphe:
    numero: int
    nombre_sommets: int
    sommets: Set[int]
    liste_sommets: List[int]
    aretes: Dict[int, list]
    matrice_adjascence: List[List[bool]]
    matrice_valeurs: List[List[Optional[int]]]
    dijkstra_possible: bool

    def __init__(self, numero: int) -> None:
        self.numero = numero
        print(f"Chargement du graphe numéro {numero} en mémoire...")
        self._lire_fichier()
        print("Graphe chargé.")
        self._initialiser_matrices()

    def _lire_fichier(self) -> None:
        """
        Lit le graphe depuis un fichier.
        Initialise :
        - le nombre de sommets,
        - la liste des sommets,
        - la valeur des différentes arêtes
        """

        # Lecture du fichier
        nom_fichier = f'L3_C1_{self.numero}.txt'
        print(f'Lecture depuis le fichier "{nom_fichier}".')
        with open(f'L3_C1_{self.numero}.txt') as f:
            lines = f.read().strip().split('\n')

        # Initialisation des sommets
        self.nombre_sommets = int(lines[0])

        self.liste_sommets = list(range(self.nombre_sommets))
        self.sommets = {*self.liste_sommets}

        # On commence avec des sommets sans aucune arêtes
        self.aretes = {i: list() for i in range(self.nombre_sommets)}

        self.dijkstra_possible = True

        # Initialisation des arêtes
        for line in lines[1:]:
            # Format d'une ligne: "SommetDépart ValeurArête SommetArrivée"
            depart, valeur, arrivee = (int(i) for i in line.split(' '))

            arete = Arete(depart, valeur, arrivee)
            self.aretes[depart].append(arete)

            # Une arête à valeur négative signifie qu'on ne peut pas utiliser Dijkstra sur le graphe
            if valeur < 0:
                self.dijkstra_possible = False

    def _initialiser_matrices(self) -> None:
        """
        Initialise la matrice d'adjascence, et la matrice de valeurs
        """
        self.matrice_adjascence = [[False for _ in range(self.nombre_sommets)] for __ in range(self.nombre_sommets)]
        self.matrice_valeurs = [[None for _ in range(self.nombre_sommets)] for __ in range(self.nombre_sommets)]

        for depart, aretes in self.aretes.items():
            for arete in aretes:
                self.matrice_adjascence[depart][arete.arrivee] = True
                self.matrice_valeurs[depart][arete.arrivee] = arete.valeur

    def dijkstra(self, depart: int) -> str:
        """
        Effectue l'algorithme de Dijkstra sur le graphe, depuis un sommet donné.
        :param depart: Le sommet à partir duquel effectuer l'algorithme.
        :return: Une représentation sous forme de string du déroulement et du résultat de l'algorithme.
        """
        resolveur = DijkstraResolveur(self.matrice_valeurs, self.liste_sommets)
        return resolveur.resoudre(depart)

    def bellman(self, depart: int) -> str:
        """
        Effectue l'algorithme de Bellman sur le graphe, depuis un sommet donné.
        :param depart: Le sommet à partir duquel effectuer l'algorithme.
        :return: Une représentation sous forme de string du déroulement et du résultat de l'algorithme.
        """
        solveur = BellmanSolveur(self.matrice_valeurs, self.liste_sommets)
        return solveur.resoudre(depart)

    def afficher(self) -> str:
        """
        Crée l'affichage du graphe, incluant ses arêtes, sa matrice d'adjascence et sa matrice de valeurs
        :return: l'affichage du graphe
        """
        affichage = f'Le graphe possède {self.nombre_sommets} sommets.\n'

        for depart, aretes in self.aretes.items():
            affichage += f'Arêtes au départ de {depart}:\n'
            for arete in aretes:
                affichage += f'\t-> Arête vers {arete.arrivee}, de valeur {arete.valeur}\n'

        affichage += "\nMatrice d'adjascence:\n"
        affichage += affichage_matrice(self.matrice_adjascence, self.liste_sommets, self.liste_sommets,
                                       {False: '0', True: '1'})

        affichage += '\nMatrice de valeurs:\n'
        affichage += affichage_matrice(self.matrice_valeurs, self.liste_sommets, self.liste_sommets, {None: ''})
        affichage += '\n'
        return affichage
