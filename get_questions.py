from query_handler import QueryHandler
import random
from os.path import exists
from queries import AVAILABLE_QUESTION_TYPES, AVAILABLE_QUERIES

handler = QueryHandler()


# def get_questions(question_type):
#     match question_type:
#         case 'dpt_code':
#             return get_dpt_code_questions()
#         case _:
#             return


# def get_dpt_code_questions(nb_questions=10):
#     question_list = []
#     option_list = []
#     answer_list = []

#     for _ in range(nb_questions):
#         element, answer_prop, answer, options = handler.generate_question(
#             question_type='dpt_code')

#         if 'code_insee' == answer_prop.removesuffix('.value'):
#             to_ask = 'Quel est le numéro du département nommé {} ?'.format(
#                 element)
#         question_list.append(to_ask)
#         options.append(answer)
#         random.shuffle(options)
#         answer_list.append(answer)
#         option_list.append(options)

#     return question_list, answer_list, option_list


def get_questions(nb_question=10, question_type=None, question_types=None):
    """Propose 'nb_question' questions et leurs réponses.

    Les questions peuvent être de type différents. Par défaut, on sélectionne aléatoirement le type de chaque question parmi les thèmes possibles.
    Si un question_type est spécifié, on ne prend que des questions de ce thème.
    Si un question_types est spécifié, on prend aléatoirement des questions parmi la liste des thèmes proposés.
    Les thèmes proposés doivent être des valeurs de code question valide, à savoir les clés du dictionnaire AVAILABLE_QUESTION_TYPES.
    """
    question_list = []
    option_list = []
    answer_list = []
    question_type_list = []

    q_spec = list(AVAILABLE_QUESTION_TYPES.keys())
    while len(question_list) < nb_question:

        q_type = question_type or random.choice(
            question_types) if question_types else None or random.choice(q_spec)

        element, answer, options = handler.generate_question(q_type)

        if AVAILABLE_QUESTION_TYPES[q_type].get('image'):
            options, answer = get_image_options(q_type, options, answer)

        # On regarde dans la fonction generate_question si la query a déjà été effectuée ou non
        # On ne s'en soucie pas ici du coup
        # element, answer_prop, answer, options = handler.generate_question(
        #     question_attr=q_spec['question_attr'],
        #     answer_attr=q_spec['answer_attr'],
        #     # FIXME: le plus simple serait de basculer le dict des queries dans le query handler
        #     query_type=q_spec['query_type'],
        #     # pour ne passer en argument que la clé, pas la longue str de la query
        #     # FIXME: à virer lorsque que la modification du dessus sera faite
        #     query=AVAILABLE_QUERIES[q_spec['query_type']]
        # )

        # FIXME: Si on veut pouvoir récupérer plusieurs attributs pour la question il faut transformer 'question_attr' en liste d'attributs
        # La méthode generate question devra le traiter en conséquence

        # FIXME: cette vérif peut maintenant être faite dans le query handler
        to_ask = AVAILABLE_QUESTION_TYPES[q_type]['question'].replace(
            'X', str(element))
        if to_ask not in (question_list):
            question_list.append(to_ask)
            options.append(answer)
            random.shuffle(options)
            answer_list.append(answer)
            option_list.append(options)
            question_type_list.append(q_type)

    return question_list, answer_list, option_list, question_type_list


def get_image_options(question_type, options, answer):
    match question_type:
        case 'code_drapeau':
            options = list(
                map(lambda code: f'assets/flags/{code}.png', options))
            answer = f'assets/flags/{answer}.png'
            return options, answer
        case 'dpt_lieu':
            options = list(
                map(lambda place: f'assets/places/{place}.png', options))
            answer = f'assets/places/{answer}.png'
            return options, answer

        case _:
            raise Exception(
                'This type of question is not supposed to return images')
