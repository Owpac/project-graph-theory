from copy import copy
from typing import List, Optional, Iterable

from L3_C1_Cellule import Cellule
from L3_C1_affichage import affichage_matrice


class DijkstraResolveur:
    sommets: List[int]
    matrice_valeurs: List[List[int]]
    cc: List[int]
    distance_dernier_sommet: int
    dernier_sommet_ajoute: int
    matrice_dijkstra: List[List[Cellule]]

    def __init__(self, matrice_valeurs: List[List[int]], sommets: Iterable[int]):
        self.matrice_valeurs = matrice_valeurs
        """ La matrice de valeurs du graphe. None représente une absence de valeur. """

        self.sommets = sorted(sommets)
        """ Une liste des sommets, dans l'ordre croissant."""

        self.cc = []
        """ Une liste des sommets actuellement dans le CC, dans l'ordre d'ajout """

        self.matrice_dijkstra = []
        """ La matrice de dijkstra, appelée pi dans l'algortithme """

        self.distance_dernier_sommet = 0
        """ Contient la distance du dernier sommet ajouté au sommet initial """

    def resoudre(self, depart: int) -> str:
        """
        Utilise l'algorithme de Dijkstra afin de trouver tous les chemins les plus courts
        depuis un sommet donné vers tous les autres.
        Utilisable dans un graphe n'ayant que des aretes aux valeurs positives ou nulles.

        :param depart: Le numéro du sommet par lequel commencer
        :return: Une représentation du déroulement de l'algorithme, ainsi que de son résultat
        """
        # Initialisation :
        #   - Seul le sommet de départ est dans CC
        #   - Il est le dernier sommet ajouté
        #   - La matrice de dijkstra (pi) ne possède qu'une seule ligne,
        #     où tous les sommets sont à une distance infinie du sommet initial (sauf lui-même)
        self.cc = [depart]
        self.dernier_sommet_ajoute = depart
        self.matrice_dijkstra = [[Cellule(0, final=False, infini=True, sommet_precedent=depart) for _ in self.sommets]]

        # La cellule de départ est directement en contact avec elle-même.
        self.matrice_dijkstra[0][depart].valeur = 0
        self.matrice_dijkstra[0][depart].infini = False

        # On sait que l'algorithme va demander un nombre d'itérations au maximum égal au nombre de sommets
        for _ in range(len(self.sommets)):
            # On crée la nouvelle ligne de la matrice de dijkstra (pi)
            self._prochaine_ligne()

            # On regarde si tous les sommets restants ont une valeur infinie
            # (ne sont pas accessibles depuis le sommet de départ).
            # Si oui, on peut arrêter l'algorithme.
            sommets_accessibles = list(
                filter(lambda cellule: not cellule.final and not cellule.infini, self.matrice_dijkstra[-1])
            )

            # S'il n'y a aucun sommet accessible, fin de l'algo
            if not sommets_accessibles:
                # Toutes les valeurs de la dernière ligne sont finales
                for sommet in self.matrice_dijkstra[-1]:
                    sommet.final = True
                break

            # On cherche le sommet ayant une distance minimum au sommet initial, et on l'ajoute au CC
            self._ajouter_sommet_minimum()

        return self._affichage()

    def _prochaine_ligne(self) -> None:
        """
        Crée et ajoute la prochaine ligne de l'algorithme à la matrice de dijkstra.
        """
        # On récupère les valeurs des arêtes issues du dernier sommet ajouté
        valeurs = self.matrice_valeurs[self.dernier_sommet_ajoute]
        ligne_precedente = self.matrice_dijkstra[-1]

        # On copie la ligne précédente (on fait une copie pour éviter que modifier une cellule en modifie d'autres)
        ligne_actuelle = [copy(ligne_precedente[sommet]) for sommet in self.sommets]
        self.matrice_dijkstra.append(ligne_actuelle)

        # On bloque l'ancienne cellule, car elle est désormais finale. Elle ne changera plus.
        ligne_actuelle[self.dernier_sommet_ajoute].final = True

        # Pour chaque sommet, s'il est successeur du dernier sommet ajouté, on met à jour sa valeur
        for sommet, valeur_arete in enumerate(valeurs):
            # Si le sommet est dans CC, pas besoin de mettre sa valeur à jour : on s'arrête
            if sommet in self.cc:
                continue

            # valeur = None signifie qu'il n'y a pas d'arête entre le dernier sommet ajouté et celui-ci.
            # L'ancienne cellule est donc toujours celle à la distance la plus courte, on n'a donc rien à faire.
            if valeur_arete is None:
                continue

            cellule_precedente = ligne_actuelle[sommet]

            # Si il y a une arete, la distance au sommet initial en passant par le dernier sommet ajouté est :
            # distance du dernier sommet ajouté + valeur de l'arete
            cellule_actuelle = Cellule(valeur_arete + self.distance_dernier_sommet, final=False, infini=False,
                                       sommet_precedent=self.dernier_sommet_ajoute)

            # La cellule de la nouvelle ligne est celle à la distance la plus courte entre la précédente et la nouvelle
            ligne_actuelle[sommet] = min(cellule_precedente, cellule_actuelle)

    def _ajouter_sommet_minimum(self) -> None:
        """
        Cherche la cellule non finale à la valeur minimum, et l'ajoute au CC
        """
        sommet_min: Cellule = Cellule(0, infini=True)
        numero_sommet_min: Optional[int] = None

        # Parmi toutes les cellules n'étant pas finales, on prend la plus petite
        for numero_sommet, cellule in enumerate(self.matrice_dijkstra[-1]):
            if not cellule.final and cellule < sommet_min:
                sommet_min = cellule
                numero_sommet_min = numero_sommet

        # On l'ajoute au CC, puis on met à jour les valeurs de distance & le numéro de la dernière cellule ajoutée
        self.cc.append(numero_sommet_min)
        self.distance_dernier_sommet = sommet_min.valeur
        self.dernier_sommet_ajoute = numero_sommet_min

    def _affichage(self) -> str:
        # Affichage du tableau de l'algorithme
        affichage = "Déroulement de l'algorithme de Dijkstra:\n"
        titres_lignes = [self.cc[:i] for i in range(len(self.cc) + 1)]
        titres_lignes = [', '.join(str(sommet) for sommet in cc) for cc in titres_lignes]
        affichage += affichage_matrice(self.matrice_dijkstra, self.sommets, titres_lignes, {}, titre="CC")

        affichage += "\n"

        affichage += "\nRésultat de l'algorithme de Dijkstra:\n"
        # Affichage du résultat de l'algorithme
        valeurs, ccs = self._resultat()
        #   Les titres des lignes sont les CC
        ccs = [None if cc is None else ' '.join(str(sommet) for sommet in cc) for cc in ccs]
        #   Les cellules n'ont pas à afficher leur prédécesseur (ce qui serait le cas normalement),
        #   donc on n'affiche que leurs valeurs
        matrice = [ccs, [v if v.infini else v.valeur for v in valeurs]]
        affichage += affichage_matrice(matrice, self.sommets, ['CC', 'Distance'], {None: '/'}, titre="Sommets")

        return affichage

    def _resultat(self):
        """
        Retourne le résultat de l'algorithme.
        :return: En premier, la valeur des chemins courts dans l'ordre des sommets
                 En deuxième, les chemins courts nécessaires pour accéder aux sommets
        """

        # Chaque sommet connaît son prédécesseur. On remonte donc jusqu'à ce qu'on trouve le sommet initial
        def chemin_court(resultat: List[Cellule], sommet: int):
            # Si le sommet n'est pas accessible, il n'y a pas de chemin court
            if self.matrice_dijkstra[-1][sommet].infini:
                return None

            sommet_precedent = resultat[sommet].sommet_precedent

            # Un seul sommet est son propre prédécesseur : le sommet initial.
            # Si cette condition est valide, on est donc arrivé au sommet initial, qui n'a qu'à se renvoyer lui-même.
            if sommet_precedent == sommet:
                return [sommet]

            # On retourne en premier le chemin court du prédécesseur, puis le sommet actuel
            return [*chemin_court(resultat, sommet_precedent), sommet]

        result = [copy(cell) for cell in self.matrice_dijkstra[-1]]
        for cell in result:
            cell.final = False

        cc = [chemin_court(result, s) for s in self.sommets]
        return result, cc
