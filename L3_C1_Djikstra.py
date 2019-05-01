from typing import List, Set, Optional
from copy import copy

from L3_C1_Cellule import Cellule
from L3_C1_affichage_graphe import affichage_matrice


class DjikstraResolveur:
    sommets: Set[int]
    liste_sommets: List[int]
    matrice_valeurs: List[List[int]]
    cc: List[int]
    valeur_cc: int
    dernier_sommet_ajoute: int
    matrice_djikstra: List[List[Cellule]]

    def __init__(self, matrice_valeurs: List[List[int]], liste_sommets: List[int]):
        self.matrice_valeurs = matrice_valeurs
        self.liste_sommets = liste_sommets
        self.sommets = set(liste_sommets)
        self.cc = []
        self.matrice_djikstra = []
        self.valeur_cc = 0

    def resoudre(self, depart: int) -> List[Cellule]:
        # Initialisation
        self.cc = [depart]
        self.dernier_sommet_ajoute = depart
        self.matrice_djikstra = [[Cellule(0, final=False, infini=True, sommet_precedent=depart) for _ in self.sommets]]

        # La cellule est directement en contact avec elle-même.
        self.matrice_djikstra[0][depart].infini = False

        for _ in range(len(self.sommets)):
            # On crée la nouvelle ligne de l'algorithme
            self.prochaine_ligne()

            # On regarde si tous les sommets restants ont une valeur infinie
            # (ne sont pas accessibles depuis le sommet de départ).
            # Si oui, on peut arrêter l'algorithme.
            sommets_accessibles = list(
                filter(lambda cellule: not cellule.final and not cellule.infini, self.matrice_djikstra[-1]))

            # S'il n'y a aucun sommet accessible, fin de l'algo
            if not sommets_accessibles:
                # Toutes les valeurs de la dernière ligne sont finales
                for sommet in self.matrice_djikstra[-1]:
                    sommet.final = True
                break

            # On cherche le sommet à la valeur de chemin minimum, et on l'ajoute au CC
            self.ajouter_sommet_minimum()

        return self.matrice_djikstra[-1]

    def prochaine_ligne(self):
        valeurs = self.matrice_valeurs[self.dernier_sommet_ajoute]
        ligne_precedente = self.matrice_djikstra[-1]

        ligne_actuelle = [copy(ligne_precedente[sommet]) for sommet in self.sommets]
        self.matrice_djikstra.append(ligne_actuelle)

        # On bloque l'ancienne cellule
        ligne_actuelle[self.dernier_sommet_ajoute].final = True

        for sommet, valeur_sommet in enumerate(valeurs):
            cellule_precedente = ligne_actuelle[sommet]

            # La valeur du sommet est
            # Valeur = None signifie que la valeur du sommet est infinie
            if valeur_sommet is None:
                cellule_actuelle = Cellule(0, final=False, infini=True)
            else:
                cellule_actuelle = Cellule(valeur_sommet + self.valeur_cc, final=False, infini=False,
                                           sommet_precedent=self.dernier_sommet_ajoute)

            # Si la nouvelle valeur est plus petite que l'ancienne valeur, et que celle-ci n'est pas finale, on remplace
            if cellule_actuelle < cellule_precedente and not cellule_precedente.final:
                ligne_actuelle[sommet] = cellule_actuelle

    def ajouter_sommet_minimum(self) -> None:
        """
        Cherche la cellule non finale à la valeur minimum, et l'ajoute au CC
        """
        sommet_min: Cellule = Cellule(0, infini=True)
        numero_sommet_min: Optional[int] = None

        for numero_sommet, cellule in enumerate(self.matrice_djikstra[-1]):
            if not cellule.final and cellule < sommet_min:
                sommet_min = cellule
                numero_sommet_min = numero_sommet

        self.cc.append(numero_sommet_min)
        self.valeur_cc = sommet_min.valeur
        self.dernier_sommet_ajoute = numero_sommet_min

    def afficher_tableau(self) -> None:
        # Affichage du tableau de l'algorithme
        titres_lignes = [self.cc[:i] for i in range(len(self.cc) + 1)]
        titres_lignes = [', '.join(str(sommet) for sommet in cc) for cc in titres_lignes]
        affichage_matrice(self.matrice_djikstra, self.liste_sommets, titres_lignes, {}, titre="CC")

    def afficher_resultat(self):
        valeurs, ccs = self.resultat()
        ccs = [None if cc is None else ' '.join(str(sommet) for sommet in cc) for cc in ccs]
        matrice = [ccs, [v if v.infini else v.valeur for v in valeurs]]
        affichage_matrice(matrice, self.liste_sommets, ['CC', 'Distance'], {None: '/'}, titre="Sommets")

    def resultat(self):
        """
        :return: En premier, la valeur des chemins courts dans l'ordre des sommets
                 En deuxième, les chemins courts nécessaires pour accéder aux sommets
        """

        def chemin_court(resultat: List[Cellule], sommet: int):
            # Si le sommet n'est pas accessible
            if self.matrice_djikstra[-1][sommet].infini:
                return None

            sommet_precedent = resultat[sommet].sommet_precedent
            if sommet_precedent == sommet:
                return [sommet]

            return [*chemin_court(resultat, sommet_precedent), sommet]

        result = [copy(cell) for cell in self.matrice_djikstra[-1]]
        for cell in result:
            cell.final = False

        cc = [chemin_court(result, s) for s in self.sommets]
        return result, cc
