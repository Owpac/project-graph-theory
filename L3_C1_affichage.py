# TODO : 4 param : matrice à afficher; titre des colonnes; titre des lignes; changement d'affichage

from itertools import chain
from typing import List, Any, Dict


def affichage_matrice(matrice: List[List[Any]], titres_colonnes: List[Any], titres_lignes: List[Any],
                      symboles=None, *, titre=None) -> str:
    """
    Affiche un graphe sous forme de tableau.
    :param titre: Le titre du tableau
    :param matrice: les données du graphe
    :type matrice: List[List[Any]]
    :param titres_colonnes: les titres des colonnes du graphe
    :param titres_lignes: les titres des lignes du graphe
    :param symboles: Un dictionnaire de symboles. La clé est le symbole lui-même, la valeur
                     est la représentation voulue de ce symbole.
    :return: Le tableau sous forme de string
    """
    affichage = ""

    if symboles is None:
        symboles = {}

    # On transforme les titres en liste de strings
    titres_colonnes: List[str] = [str(titre) for titre in titres_colonnes]
    titres_lignes: List[str] = [str(titre) for titre in titres_lignes]

    matrice_aplatie: List[Any] = [valeur for ligne in matrice for valeur in ligne]

    # On récupère la taille maximum de ce qui va être affiché dans le tableau, afin de faire
    # des cellules ayant toutes la même taille
    cellules = chain((affichage_valeur(v, symboles) for v in matrice_aplatie), titres_colonnes)

    taille_maximum = max(map(len, cellules))

    taille_titre_ligne = max(map(len, titres_lignes + [str(titre)]))

    # On ajoute 2 à la taille maximum, afin qu'il y ai de l'espace entre les valeurs et les bordures
    taille_maximum += 2
    taille_titre_ligne += 2

    affichage += affichage_delimiteur(len(titres_colonnes), taille_maximum, taille_titre_ligne, decalage=titre is None)

    # Affichage de la première ligne, qui possède les titres des colonnes
    if titre is None:
        affichage += " " * (taille_titre_ligne + 1) + "|"
    else:
        affichage += "|{:^{}}".format(titre, taille_titre_ligne) + '|'

    for titre in titres_colonnes:
        affichage += "{:^{}}".format(titre, taille_maximum) + "|"

    affichage += "\n"

    affichage += affichage_delimiteur(len(titres_colonnes), taille_maximum, taille_titre_ligne)

    # Affichage ligne
    for titre, ligne in zip(titres_lignes, matrice):

        # Affichage du titre de la ligne, de manière centrée
        affichage += "| {:<{}}".format(titre, taille_titre_ligne - 1) + "|"

        # Affichage des valeurs de la ligne, en les forçant à s'afficher le plus à droite possible.
        # On retire 1 à la taille maximum (qui est déjà de 2 de plus que la vraie taille maximum),
        # et on force l'espace à se trouver à droite. Ainsi elles s'affichent à droite,
        # mais elles sont tout de même éloignées de la bordure (question esthétique).
        for valeur in ligne:
            format_string = " {:^{}}"
            taille_valeur = taille_maximum - 2

            if len(str(valeur)) % 2 == 0 and taille_valeur % 2 == 1:
                format_string = " " + format_string
                taille_valeur -= 1

            affichage += format_string.format(affichage_valeur(valeur, symboles), taille_valeur) + " |"

        affichage += "\n"

    affichage += affichage_delimiteur(len(titres_colonnes), taille_maximum, taille_titre_ligne)

    # On remplace les caractères Unicode causant un décalage par un ensemble de caractères Unicode sans décalage
    return affichage


def affichage_delimiteur(nombre_colonne: int, taille: int, taille_titre_ligne: int, *, decalage: bool = False) -> str:
    """
    Affiche une ligne de délimiteurs
    :param nombre_colonne: Le nombre de colonnes
    :param taille: La largeur maximale d'une cellule du corps du tableau
    :param taille_titre_ligne: La largeur maximale d'une cellule des titres des lignes
    :param decalage: S'il faut un décalage (un blanc) au début de la ligne
    :return: Une représentation sous forme de string de cette ligne de délimiteurs
    """
    affichage = ""
    if decalage:
        affichage += " " * (taille_titre_ligne + 1) + "+"
    else:
        affichage += "+" + "-" * taille_titre_ligne + "+"

    for i in range(nombre_colonne):
        affichage += "-" * taille + "+"

    affichage += "\n"
    return affichage


def affichage_valeur(valeur: Any, symboles: Dict[Any, str]) -> str:
    """
    Affiche une valeur donnée, où son symbole associé si celui-ci existe.
    :param valeur: La valeur à afficher
    :param symboles: Un dictionnaire de symboles. La clé est le symbole lui-même, la valeur
                     est la représentation voulue de ce symbole.
    :return: La représentation de la valeur.
    """
    try:
        # Si la valeur possède un symbole associé, on envoie le symbole
        if valeur in symboles and type(valeur) is not int:
            return str(symboles[valeur])
    except TypeError:
        # Si la valeur n'est pas "hashable" (ne peut pas être contenue dans un dictionnaire),
        # on la renvoie simplement
        pass

    return str(valeur)
