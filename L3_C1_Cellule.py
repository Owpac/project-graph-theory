# Created by Florian on 17/04/2019
from typing import Optional, Union


class Cellule:
    """
    Une Cellule est une cellule du tableau de Dijkstra ou Bellman.
    Elle contient notamment la distance du sommet actuel au sommet initial, si celle-ci est infinie ou finale,
    et son prédécesseur dans le chemin court.
    """
    valeur: int
    final: bool
    infini: bool
    sommet_precedent: Optional[int]

    def __init__(self, valeur: int, *, final=False, infini=False, sommet_precedent: Optional[int] = None):
        """
        Crée une nouvelle Cellule.
        :param valeur: la distance actuelle du sommet au sommet initial
        :param final: si la distance est la distance finale, celle qui sera dans pi étoile
        :param infini: si la distance est infinie ou non (auquel cas la valeur donnée ne compte pas)
        :param sommet_precedent: le sommet précédent dans le CC
        """
        self.valeur = valeur
        self.final = final
        self.infini = infini
        self.sommet_precedent = sommet_precedent

    def __eq__(self, other: Union['Cellule', int]):
        # Si on compare avec un entier, on compare juste les valeurs
        if isinstance(other, int):
            return self.valeur == other

        # Deux cellules sont égales si elles ont le même infini (vrai/faux), et la même valeur
        return (self.infini == other.infini) and (self.valeur == other.valeur)

    def __lt__(self, other: Union['Cellule', int]):
        # Si on compare avec un entier, on compare juste les valeurs
        if isinstance(other, int):
            return not self.infini and self.valeur < other

        # Deux infinis ne sont pas inférieurs l'un à l'autre
        if other.infini and self.infini:
            return False

        # Si le nombre actuel est infini et l'autre non, alors il n'est pas inférieur
        if self.infini and not other.infini:
            return False

        # Si le nombre actuel n'est pas infini mais l'autre si, alors il est inférieur
        if other.infini and not self.infini:
            return True

        # Sinon, on retourne juste la comparaison des valeurs
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

        # Une cellule s'affiche en mettant la valeur jusqu'au sommet initial puis le prédecesseur.
        # Ex: 5(0) -> il y a une distance de 5 entre le sommet initial et le sommet actuel, et le prédecesseur est 0
        return f'{self.valeur}({self.sommet_precedent})'
