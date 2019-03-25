from '' import poser_question


def main():
    continuer = True
    while continuer:
        continuer = poser_question('Voulez-vous tester un autre graphe ?')


if __name__ == '__main__':
    main()
