from L3_C1_Graphe import Graphe
from L3_C1_entree_utilisateur import poser_question, demander_nombre


def main():
    continuer = True
    nombre_graphes = 10

    while continuer:
        print("Quel graphe voulez-vous tester ?")
        numero = demander_nombre(1, nombre_graphes)

        graphe = Graphe(numero)
        graphe.afficher()

        print('\n====== Calcul du plus court chemin ======')
        if graphe.dijkstra_possible:
            print("Le graphe ne possède pas d'arête à valeur négative.")
            print("Vous pouvez donc choisir l'algorithme :")
            print("1. Dijkstra")
            print("2. Bellman")
            algo_choisi = demander_nombre(1, 2)
        else:
            print("Le graphe possède une arête à valeur négative. On utilisera donc l'algortihme de Bellman.")
            algo_choisi = 2

        print('\nPar quel sommet commencer ?')
        print('Sommets possibles:', *graphe.sommets)
        depart = demander_nombre(0, graphe.nombre_sommets - 1)

        fichier_trace = f'L3_C1_trace_{numero}_{depart}.txt'
        with open(fichier_trace, mode='w', encoding='utf-8') as f:
            if algo_choisi == 1:
                annonce = f"Vous avez choisi l'algorithme de Dijkstra, partant du sommet {depart}\n"
                resultat = graphe.dijkstra(depart)
            else:
                annonce = f"Vous avez choisi l'algorithme de Bellman, partant du sommet {depart}\n"
                resultat = graphe.bellman(depart)
            print(annonce)
            print(resultat)

            # On enregistre les traces d'exécution
            print(annonce, file=f)
            print(resultat, file=f)

            print(f"Enregistrement des traces d'exécution dans le fichier \"{fichier_trace}\" effectué.")

        continuer = poser_question('Voulez-vous tester un autre graphe ?')


if __name__ == '__main__':
    main()
