# TODO : 4 param : matrice à afficher; titre des colonnes; titre des lignes; changement d'affichage

from typing import List, Any, Dict
from itertools import chain


def affichage_matrice(matrice: List[List[Any]], titres_colonnes: List[Any], titres_lignes: List[Any],
                      symboles=None, *, titre=None) -> None:
    """
    Affiche un graphe sous forme de tableau.
    :param matrice: les données du graphe
    :type matrice: List[List[Any]]
    :param titres_colonnes: les titres des colonnes du graphe
    :param titres_lignes: les tritres des lignes du graphe
    :param symboles: les symboles que l'on doit afficher différemment dans la console.

    :return:
    """

    if symboles is None:
        symboles = {}

    # On transforme les titres en liste de strings
    titres_colonnes: List[str] = [str(titre) for titre in titres_colonnes]
    titres_lignes: List[str] = [str(titre) for titre in titres_lignes]

    taille_titre_ligne = 0
    taille_maximum: int = 0

    matrice_aplatie: List[Any] = [valeur for ligne in matrice for valeur in ligne]

    # On récupère la taille maximum de ce qui va être affiché dans le tableau, afin de faire
    # des cellules ayant toutes la même taille
    cellules = chain((affichage_valeur(v, symboles) for v in matrice_aplatie), titres_colonnes)

    taille_maximum = max(map(len, cellules))

    taille_titre_ligne = max(map(len, titres_lignes + [str(titre)]))

    # On ajoute 2 à la taille maximum, afin qu'il y ai de l'espace entre les valeurs et les bordures
    taille_maximum += 2
    taille_titre_ligne += 2

    affichage_delimiteur(len(titres_colonnes), taille_maximum, taille_titre_ligne, decalage=titre is None)

    # Affichage de la première ligne, qui possède les titres des colonnes
    if titre is None:
        print(" " * (taille_titre_ligne + 1), end="|")
    else:
        print("|{:^{}}".format(titre, taille_titre_ligne), end='|')

    for titre in titres_colonnes:
        print("{:^{}}".format(titre, taille_maximum), end="|")

    print()

    affichage_delimiteur(len(titres_colonnes), taille_maximum, taille_titre_ligne)

    # Affichage ligne
    for titre, ligne in zip(titres_lignes, matrice):

        # Affichage du titre de la ligne, de manière centrée
        print("| {:<{}}".format(titre, taille_titre_ligne - 1), end="|")

        # Affichage des valeurs de la ligne, en les forçant à s'afficher le plus à droite possible.
        # On retire 1 à la taille maximum (qui est déjà de 2 de plus que la vraie taille maximum),
        # et on force l'espace à se trouver à droite. Ainsi elles s'affichent à droite,
        # mais elles sont tout de même éloignées de la bordure (question esthétique).
        for valeur in ligne:
            print("{:>{}}".format(affichage_valeur(valeur, symboles), taille_maximum - 1), end=" |")

        print()

    affichage_delimiteur(len(titres_colonnes), taille_maximum, taille_titre_ligne)


def affichage_delimiteur(nombre_colonne: int, taille: int, taille_titre_ligne: int, *, decalage: bool = False) -> None:
    if decalage:
        print(" " * (taille_titre_ligne + 1), end="+")
    else:
        print("+" + "-" * taille_titre_ligne, end="+")

    for i in range(nombre_colonne):
        print("-" * taille, end="+")

    print()


def affichage_valeur(valeur: Any, symboles: Dict[Any, str]) -> str:
    """

    :param valeur:
    :param symboles:
    :return:
    """
    try:
        if valeur in symboles and type(valeur) is not int:
            return str(symboles[valeur])
    except TypeError:
        # Si la valeur n'est pas "hashable" (ne peut pas être contenue dans un dictionnaire),
        # on la renvoie simplement
        pass

    return str(valeur)
