# Created by Florian on 01/05/2019
from typing import List, Generator, Optional

from L3_C1_Cellule import Cellule
from L3_C1_affichage import affichage_matrice


class BellmanSolveur:
    matrice_valeurs: List[List[int]]
    sommets: List[int]
    pi: List[List[Cellule]]

    def __init__(self, matrice_valeurs: List[List[int]], liste_sommets: List[int]):
        self.matrice_valeurs = matrice_valeurs
        self.sommets = liste_sommets

    def resoudre(self, depart: int) -> str:
        """
        Utilise l'algorithme de Bellman afin de trouver tous les chemins les plus courts
        depuis un sommet donné vers tous les autres.
        Utilisable dans un graphe ayant des aretes aux valeurs quelconques.

        :param depart: Le numéro du sommet par lequel commencer
        :return: Une représentation du déroulement de l'algorithme, ainsi que de son résultat
        """

        # On commence par créer la matrice carrée pi, une liste en 2D de taille le nombre de sommets
        self.pi = [[Cellule(0, infini=True) for _ in self.sommets]]
        # Le sommet initial est à une distance 0 de lui-même
        self.pi[0][depart] = Cellule(0, sommet_precedent=depart)

        # On sait à l'avance que k sera au maximum égal au nombre de sommets.
        # Si on trouve une condition de sortie normale (ligne k-1 == ligne k), on retourne directement le résultat
        # Ainsi, si on sort de la boucle for, cela veut dire qu'aucune condition de sortie normale n'a été trouvée.
        # Il y aurait donc un circuit absorbant.
        #
        # On a besoin de faire n itérations, car au maximum (dans un graphe sans circuit absorbant), Bellman trouvera
        # les chemins courts à la n-1ième itération. Il faut donc une dernière itération pour vérifier que
        # l'itération n-1 est bien la bonne. Si elle ne l'est pas, il y a un circuit absorbant.
        for k in range(1, len(self.sommets) + 1):
            nouvelle_ligne = [Cellule(0, infini=True) for _ in self.sommets]

            for i in self.sommets:
                # Pour tout sommet autre que celui de départ, on choisit comme poids courant le minimum entre :
                # - son poids à l’itération précédente et
                # - les poids obtenus en passant par tous ses prédécesseurs
                #   dont les poids ont changé à l’itération précédente
                valeurs_depuis_predecesseurs = []
                for j in self.predecesseurs(i):
                    if self.pi[-1][j].infini:
                        continue
                    valeur = self.pi[-1][j].valeur + self.matrice_valeurs[j][i]
                    valeurs_depuis_predecesseurs.append(Cellule(valeur, sommet_precedent=j))

                nouvelle_ligne[i] = min((self.pi[-1][i], *valeurs_depuis_predecesseurs))

            # On rajoute la nouvelle ligne à la matrice de dijkstra
            self.pi.append(nouvelle_ligne)

            # L'algorithme se termine quand une itération est similaire à la précédente
            if nouvelle_ligne == self.pi[-2]:
                # Affichage d'abord du déroulement de l'algorithme :
                affichage = "Déroulement de l'algorithme de Bellman:\n"
                affichage += affichage_matrice(self.pi, self.sommets, list(range(len(self.pi))), titre='k')
                ccs = self.trouver_cc()
                ccs = [None if cc is None else ' '.join(str(sommet) for sommet in cc) for cc in ccs]

                # Puis du tableau de résultat
                affichage += "\nRésultat de l'algorithme de Bellman:\n"
                affichage += affichage_matrice([ccs, [v if v.infini else v.valeur for v in self.pi[-1]]],
                                               self.sommets, ['CC', 'Distance'], {None: '/'}, titre="Sommets")
                return affichage

        # Aucune sortie n'a été effectuée dans la boucle. Il ya donc un circuit absorbant.
        affichage = "Déroulement de l'algorithme de Bellman:\n"
        affichage += affichage_matrice(self.pi, self.sommets, list(range(len(self.pi))), titre='k')
        affichage += "Impossible de continuer plus loin : présence d'un circuit absorbant." + "\n"
        return affichage

    def predecesseurs(self, i: int) -> Generator[int, None, None]:
        """
        Renvoie les prédécesseurs d'un sommet donné
        :param i: le numéro du sommet dont il faut trouver les prédécesseurs
        :return: un générateur de prédécesseurs
        """
        for potentiel_predecesseur in range(len(self.matrice_valeurs[i])):
            if self.matrice_valeurs[potentiel_predecesseur][i] is not None:
                yield potentiel_predecesseur

    def trouver_cc(self) -> List[Optional[List[int]]]:
        """
        Trouve, pour chaque sommet, une liste des sommets à parcourir
        afin de faire le chemin le plus court depuis le sommet initial.
        :return: Une liste possédant, pour chaque sommet :
                 - Soit None, ce qui veut dire que le sommet n'est pas atteignable depuis le sommet initial
                 - Une liste de numéros de sommets à suivre, formant le chemin le plus court depuis le sommet initial
        """

        def chemin_court(resultat: List[Cellule], sommet: int) -> Optional[List[int]]:
            # Si le sommet n'est pas accessible
            if resultat[sommet].infini:
                return None

            sommet_precedent = resultat[sommet].sommet_precedent
            if sommet_precedent == sommet:
                return [sommet]

            return [*chemin_court(resultat, sommet_precedent), sommet]

        return [chemin_court(self.pi[-1], s) for s in self.sommets]
