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
