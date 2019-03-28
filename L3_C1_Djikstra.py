from typing import List, Set, Optional, Dict

from copy import copy


class Cellule:
    valeur: int
    final: bool
    infini: bool
    sommet_precedent: Optional[int]

    def __init__(self, valeur: int, *, final=False, infini=False, sommet_precedent: Optional[int] = None):
        self.valeur = valeur
        self.final = final
        self.infini = infini
        self.sommet_precedent = sommet_precedent

    def __eq__(self, other: 'Cellule'):
        return (self.infini == other.infini) or (self.valeur == other.valeur)

    def __lt__(self, other: 'Cellule'):
        # Deux infinis ne sont pas inférieurs l'un à l'autre
        if other.infini and self.infini:
            return False

        # Si le nombre actuel est infini et l'autre non, alors il n'est pas inférieur
        if self.infini and not other.infini:
            return False

        # Si le nombre actuel n'est pas infini mais l'autre si, alors il est inférieur
        if other.infini and not self.infini:
            return True

        return self.valeur < other.valeur

    def __le__(self, other: 'Cellule'):
        return self < other or self == other

    def __gt__(self, other: 'Cellule'):
        return not self <= other

    def __ge__(self, other: 'Cellule'):
        return not self < other

    def __str__(self):
        if self.infini:
            return '∞'
        if self.final:
            return '•'
        return f'{self.valeur}({self.sommet_precedent})'


class DjikstraResolveur:
    sommets: Set[int]
    matrice_valeurs: List[List[int]]
    cc: List[int]
    valeur_cc: int
    dernier_sommet_ajoute: int
    matrice_djikstra: List[List[Cellule]]

    def __init__(self, matrice_valeurs: List[List[int]], sommets: Set[int]):
        self.matrice_valeurs = matrice_valeurs
        self.sommets = sommets
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
            self.prochaine_ligne()
            self.ajouter_sommet_minimum()

        return self.matrice_djikstra[-1]

    def prochaine_ligne(self):
        valeurs = self.matrice_valeurs[self.dernier_sommet_ajoute]
        ligne_precedente = self.matrice_djikstra[-1]

        ligne_actuelle = [copy(ligne_precedente[sommet]) for sommet in self.sommets]
        self.matrice_djikstra.append(ligne_actuelle)

        # On bloque l'ancienne cellule
        ligne_actuelle[self.dernier_sommet_ajoute].final = True

        for sommet, valeur in enumerate(valeurs):
            # Si on est à la 1ère ligne, l'ancienne ligne n'est composée que de valeurs infinies
            cellule_precedente = ligne_actuelle[sommet]

            # La valeur actuelle est celle de la matrice de valeurs. Si il n'y a pas de valeur, alors c'est un infini.
            if valeur is None:
                cellule_actuelle = Cellule(0, final=False, infini=True)
            else:
                cellule_actuelle = Cellule(valeur + self.valeur_cc, final=False, infini=False,
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

    def __repr__(self) -> str:
        representation = []
        for i, ligne in enumerate(self.matrice_djikstra):
            representation.append(str(self.cc[:i]) + ': ' + ' '.join(str(cell) for cell in ligne))

        return '\n'.join(representation)

    def resultat(self):
        def chemin_court(resultat: List[Cellule], sommet: int):
            sommet_precedent = resultat[sommet].sommet_precedent
            if sommet_precedent == sommet:
                return [sommet]

            return [*chemin_court(resultat, sommet_precedent), sommet]

        result = [copy(cell) for cell in self.matrice_djikstra[-1]]
        for cell in result:
            cell.final = False

        cc = [chemin_court(result, s) for s in self.sommets]
        return result, cc
