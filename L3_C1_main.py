from L3_C1_entree_utilisateur import poser_question, demander_nombre

from L3_C1_Graphe import Graphe


def main():
    continuer = True
    while continuer:
        print("Quel graphe voulez-vous charger ?")
        numero = demander_nombre(0, 15)
        graphe = Graphe(numero)

        continuer = poser_question('Voulez-vous tester un autre graphe ?')


if __name__ == '__main__':
    main()
