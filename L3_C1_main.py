from L3_C1_entree_utilisateur import poser_question, demander_nombre

from L3_C1_Graphe import Graphe


def main():
    continuer = True
    while continuer:
        print("Quel graphe voulez-vous charger ?")
        numero = demander_nombre(0, 15)
        graphe = Graphe(numero)

        print('====== Calcul du plus court chemin ======')
        algo_choisi = 2
        if graphe.djikstra_possible:
            print("Le graphe ne possède pas d'arête à valeur négative.")
            print("Vous pouvez donc choisir l'algorithme :")
            print("1. Djikstra")
            print("2. Bellman")
            algo_choisi = demander_nombre(1, 2)
        else:
            print("Le graphe possède une arête à valeur négative. On utilisera donc l'algortihme de Bellman.")

        print('\nPar quel sommet commencer ?')
        print('Sommets possibles:', *graphe.sommets)
        depart = demander_nombre(0, graphe.nombre_sommets - 1)

        if algo_choisi == 1:
            print(f"Vous avez choisi l'algorithme de Djikstra, partant du sommet {depart}")
            graphe.djikstra(depart)
        else:
            print(f"Vous avez choisi l'algorithme de Bellman, partant du sommet {depart}")
            graphe.bellman(depart)

        continuer = poser_question('Voulez-vous tester un autre graphe ?')


if __name__ == '__main__':
    main()
