# Created by Florian on 01/05/2019
from typing import List

from L3_C1_Cellule import Cellule
from L3_C1_affichage_graphe import affichage_matrice


class BellmanSolveur:
    matrice_valeurs: List[List[int]]
    liste_sommets: List[int]
    pi: List[List[Cellule]]

    def __init__(self, matrice_valeurs: List[List[int]], liste_sommets: List[int]):
        self.matrice_valeurs = matrice_valeurs
        self.liste_sommets = liste_sommets

    def resoudre(self, depart: int):
        self.pi = [[Cellule(0, infini=True) for colonne in self.liste_sommets] for ligne in self.liste_sommets]
        for i in self.liste_sommets:
            self.pi[i][depart] = Cellule(0, sommet_precedent=depart)

        k = 1
        while True:
            for i in self.liste_sommets:
                # Pour tout sommet autre que celui de départ, on choisit comme poids courant le minimum entre :
                # - son poids à l’itération précédente et
                # - les poids obtenus en passant par tous ses prédécesseurs
                #   dont les poids ont changé à l’itération précédente
                valeurs_depuis_predecesseurs = []
                for j in self.predecesseurs(i):
                    if self.pi[k - 1][j].infini:
                        continue
                    if self.matrice_valeurs[j][i] is None:
                        continue
                    valeur = self.pi[k - 1][j].valeur + self.matrice_valeurs[j][i]
                    valeurs_depuis_predecesseurs.append(Cellule(valeur, sommet_precedent=j))

                self.pi[k][i] = min(self.pi[k - 1][i],
                                    min(valeurs_depuis_predecesseurs or [Cellule(0, infini=True)]))
            if self.pi[k] == self.pi[k - 1]:
                self.pi = self.pi[:k + 1]
                affichage_matrice(self.pi, self.liste_sommets, list(range(k)), titre='k')
                ccs = self.trouver_cc()
                ccs = [None if cc is None else ' '.join(str(sommet) for sommet in cc) for cc in ccs]
                affichage_matrice([ccs, self.pi[-1]], self.liste_sommets, ['CC', 'Distance'], {None: '/'}, titre="Sommets")
                break
            k += 1

            if k == len(self.liste_sommets):
                affichage_matrice(self.pi, self.liste_sommets, list(range(k)), titre='k')
                print("Impossible de continuer plus loin : présence d'un circuit absorbant.")
                return

    def predecesseurs(self, i: int) -> List[int]:
        for potentiel_predecesseur in range(len(self.matrice_valeurs[i])):
            if self.matrice_valeurs[potentiel_predecesseur][i] is not None:
                yield potentiel_predecesseur

    def trouver_cc(self):
        def chemin_court(resultat: List[Cellule], sommet: int):
            # Si le sommet n'est pas accessible
            if resultat[sommet].infini:
                return None

            sommet_precedent = resultat[sommet].sommet_precedent
            if sommet_precedent == sommet:
                return [sommet]

            return [*chemin_court(resultat, sommet_precedent), sommet]

        return [chemin_court(self.pi[-1], s) for s in self.liste_sommets]
