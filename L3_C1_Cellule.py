# Created by Florian on 17/04/2019
from typing import Optional


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
