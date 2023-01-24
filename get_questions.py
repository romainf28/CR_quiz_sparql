from query_handler import QueryHandler
import random

handler = QueryHandler()


# Un code question a une typologie de type 'x_y' pour une question 'quel est le y de l'objet x ?'
# AVAILABLE_QUESTION_TYPES est un dictionnaire qui permet de construire la fonction de génération de question avec ses réponses.
# C'est un dictionnaire (ou json), ayant un attribut par type de question possible.
# Pour chaque type de question on va retrouver 
# answer_attr : le nom de colonne espéré de la réponse
# query_type : à valeur dans ['departement', 'commune', 'drapeau'], indique dans quelle query ou df chercher la réponse
# question : intitulé de la question à poser. Doit contenir un X majuscule qui sera remplacé par la donnée de l'énoncé

AVAILABLE_QUESTION_TYPES = {
    'dpt_code': {
        'answer_attr': 'code_insee',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département X ?'
    },
    'code_dpt': {
        'answer_attr': 'departementLabel',
        'query_type': 'departement',
        'question': 'Quel est le département correspondant au numéro X ?'
    },
    'dpt_capitale': {
        'answer_attr': 'capitaleLabel',
        'query_type': 'departement',
        'question': 'Quelle est la capitale du département X ?'
    }, 
    'dpt_population': {
        'answer_attr': 'Population',
        'query_type': 'departement',
        'question': 'Quelle est la population du département X ?'
    },
    'dpt_surface': {
        'answer_attr': 'Area',
        'query_type': 'departement',
        'question': 'Quelle est la surface du département X ?'
    },
    'dpt_drapeau': {
        'answer_attr': 'drapeau',
        'query_type': 'departement',
        'question': 'Quel est le drapeau du département X ?'
    },
    'cmn_region': {
        'answer_attr': 'regionLabel',
        'query_type': 'commune',
        'question': 'A quelle région appartient la commune X ?'
    }, 
    'cmn_dpt': {
        'answer_attr': 'departementLabel',
        'query_type': 'commune',
        'question': 'A quel département appartient la commune X ?'
    },
    'cmn_population': {
        'answer_attr': 'communePopulation',
        'query_type': 'commune',
        'question': 'Quelle est la population de la commune X ?'
    },
    'cmn_code': {
        'answer_attr': 'codecommune',
        'query_type': 'commune',
        'question': 'Quel est le code commune de la commune X ?'
    },
    'code_cmn': {
        'answer_attr': 'communeLabel',
        'query_type': 'commune',
        'question': 'Quelle commune correspond au code commune X ?'
    }
}


query_dpt = """

"""

query_cmn = """

"""

query_drp = """

"""

# Si une query est faite pour chaque question générée
AVAILABLE_QUERIES = {
    'departement': query_dpt,
    'commune': query_cmn, 
    'drapeau': query_drp
}

# Si les queries sont exécutées puis stockées
AVAILABLE_DATAFRAMES = {
    'departement': None,
    'commune': None,
    'drapeau': None
} 

# On peut avoir besoin des deux dans le cas où on exécute la query la 1ere fois qu'on la croise puis qu'on stocke le résultat pour ne pas avoir à la réexécuter.


def get_questions(question_type):
    match question_type:
        case 'dpt_code':
            return get_dpt_code_questions()
        case _:
            return


def get_dpt_code_questions(nb_questions=10):
    question_list = []
    option_list = []
    answer_list = []

    for _ in range(nb_questions):
        element, answer_prop, answer, options = handler.generate_question(question_type='dpt_code')

        if 'code_insee' == answer_prop.removesuffix('.value'):
            to_ask = 'Quel est le numéro du département nommé {} ?'.format(
                element)
        question_list.append(to_ask)
        options.append(answer)
        random.shuffle(options)
        answer_list.append(answer)
        option_list.append(options)

    return question_list, answer_list, option_list
