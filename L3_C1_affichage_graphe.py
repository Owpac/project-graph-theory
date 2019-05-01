# TODO : 4 param : matrice à afficher; titre des colonnes; titre des lignes; changement d'affichage

from typing import List, Any, Dict


def affichage_matrice(matrice: List[List[Any]], titres_colonnes: list, titres_lignes: list,
                      symboles: Dict[Any, str]) -> None:
    """
    Affiche un graphe sous forme de tableau.
    :param matrice: les données du graphe
    :type matrice: List[List[Any]]
    :param titres_colonnes: les titres des colonnes du graphe
    :param titres_lignes: les tritres des lignes du graphe
    :param symboles: les symboles que l'on doit afficher différemment dans la console.

    :return:
    """

    taille_maximum: int = 0

    applatissement_matrice: List[Any] = [valeur for ligne in matrice for valeur in ligne]

    valeurs = applatissement_matrice + titres_colonnes + titres_lignes

    for valeur in valeurs:
        taille: int = len(str(valeur))

        if taille > taille_maximum:
            taille_maximum = 3 + taille

    print()

    affichage_delimiteur(len(titres_colonnes), taille_maximum, True)

    # Affichage colonne
    print(" " * (taille_maximum - 1), end="|")

    for titre in titres_colonnes:
        print("{:^{}}".format(titre, taille_maximum - 1), end="|")

    print()

    affichage_delimiteur(len(titres_colonnes), taille_maximum)

    # Affichage ligne
    for ligne in matrice:

        print("{}{:^{}}".format("|", titres_lignes[matrice.index(ligne)], taille_maximum - 2), end="|")

        for valeur in ligne:
            print("{:>{}}".format(affichage_valeur(valeur, symboles), taille_maximum - 2), end=" |")

        print()

    affichage_delimiteur(len(titres_colonnes), taille_maximum)

    print()


def affichage_delimiteur(nombre_colonne: int = 0, taille: int = 0, decalage: bool = False) -> None:
    """

    :param nombre_colonne:
    :param taille:
    :param decalage:
    :return:
    """
    if decalage:
        print(" " * (taille - 1), end="+")
    else:
        print("{}{:-<{}}".format("+", "", taille - 2), end="+")

    for i in range(nombre_colonne):
        print("{:-<{}}".format("", taille - 1), end="+")

    print()


def affichage_valeur(valeur: Any, symboles: Dict[Any, str]) -> str:
    """

    :param valeur:
    :param symboles:
    :return:
    """
    if valeur in symboles and type(valeur) is not int:
        return str(symboles[valeur])
    else:
        return str(valeur)
