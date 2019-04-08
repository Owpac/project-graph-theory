# Created by Florian on 25/03/2019


def poser_question(question: str) -> bool:
    """
    Pose une question à l'utilisateur, qui doit répondre par oui ou non.
    :param question: La question à poser à l'utilisateur
    :return: La réponse utilisateur
    """
    while True:
        entree_utilisateur = input(question + ' (oui/non, 1/0, o/n)\n> ').lower()

        if entree_utilisateur in ('o', '1', 'yes', 'oui'):
            return True

        if entree_utilisateur in ('n', '0', 'no', 'non'):
            return False

        print('Réponse incorrecte. Veuillez rentrer : oui/non, 1/0, o/n')


def demander_nombre(mini: int = None, maxi: int = None) -> int:
    """
    Demande un nombre à l'utilisateur, situé entre min et max.
    :param mini: le minimum
    :param maxi: le maximum
    :return:
    """
    message = 'Veuillez rentrer un nombre:'
    if mini is not None and maxi is not None:
        message = f'Veuillez rentrer un nombre entre {mini} et {maxi}:'
    elif mini is not None and maxi is None:
        message = f'Veuillez rentrer un nombre supérieur à {mini}:'

    while True:
        nombre = input(message + '\n> ')

        # On s'assure que l'utilisateur vient de rentrer un nombre
        try:
            # On convertit en nombre base 10
            nombre = int(nombre)
        except ValueError:
            print('Valeur incorrecte.')
            continue

        # Le nombre est désormais un entier. On vérifie qu'il coincide avec les valeurs min/max
        if mini is not None and nombre < mini:
            print(f'Le nombre entré est trop petit. Il doit valoir au moins {mini}')
        elif maxi is not None and nombre > maxi:
            print(f'Le nombre entré est trop grand. Il doit valoir au maximum {maxi}')
        else:
            return nombre
