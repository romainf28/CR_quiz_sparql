from query_handler import QueryHandler
import random
from os.path import exists

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
        'question_attr': 'departementLabel',
        'answer_attr': 'code_insee',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département X ?'
    },
    'code_dpt': {
        'question_attr': 'code_insee',
        'answer_attr': 'departementLabel',
        'query_type': 'departement',
        'question': 'Quel est le département correspondant au numéro X ?'
    },
    'dpt_capitale': {
        'question_attr': 'departementLabel',
        'answer_attr': 'capitaleLabel',
        'query_type': 'departement',
        'question': 'Quelle est la capitale du département X ?'
    }, 
    'dpt_population': {
        'question_attr': 'departementLabel',
        'answer_attr': 'Population',
        'query_type': 'departement',
        'question': 'Quelle est la population du département X ?'
    },
    'dpt_surface': {
        'question_attr': 'departementLabel',
        'answer_attr': 'Area',
        'query_type': 'departement',
        'question': 'Quelle est la surface du département X ?'
    },
    'dpt_drapeau': {
        'question_attr': 'departementLabel',
        'answer_attr': 'drapeau',
        'query_type': 'drapeau',
        'question': 'Quel est le drapeau du département X ?'
    },
    'cmn_region': {
        'question_attr': 'communeLabel',
        'answer_attr': 'regionLabel',
        'query_type': 'commune',
        'question': 'A quelle région appartient la commune X ?'
    }, 
    'cmn_dpt': {
        'question_attr': 'communeLabel',
        'answer_attr': 'departementLabel',
        'query_type': 'commune',
        'question': 'A quel département appartient la commune X ?'
    },
    'cmn_population': {
        'question_attr': 'communeLabel',
        'answer_attr': 'communePopulation',
        'query_type': 'commune',
        'question': 'Quelle est la population de la commune X ?'
    },
    'cmn_code': {
        'question_attr': 'communeLabel',
        'answer_attr': 'codecommune',
        'query_type': 'commune',
        'question': 'Quel est le code commune de la commune X ?'
    },
    'code_cmn': {
        'question_attr': 'codecommune',
        'answer_attr': 'communeLabel',
        'query_type': 'commune',
        'question': 'Quelle commune correspond au code commune X ?'
    },
    'lieu_dpt': {
        'question_attr': 'lieu',
        'answer_attr': 'departementLabel',
        'query_type': 'lieu',
        'question': 'Dans quel département se situe le lieu X ?'
    }
}

query_gen = """SELECT DISTINCT ?code_insee ?departementLabel ?drapeau ?Area ?capitaleLabel ?departementPopulation ?regionLabel

                WHERE {
                    VALUES ?type {  wd:Q6465 wd:Q202216  }

                    ?departement wdt:P31 ?type;
                    wdt:P36 ?capitale;
                    wdt:P1082 ?departementPopulation;
                    wdt:P2586 ?code_insee;
                    wdt:P2046 ?Area.
                    
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                    }
                        
                    ORDER BY ?code_insee"""

query_cmn = """
                SELECT DISTINCT ?departementLabel ?communeLabel ?regionLabel ?code_insee
                WHERE {
                    VALUES ?type {  wd:Q6465 wd:Q202216  }

                    ?departement wdt:P31 ?type;
                    wdt:P2586 ?code_insee.

                    ?commune wdt:P31 wd:Q484170;
                    wdt:P1082 ?communePopulation.
                    
                    ?region wdt:P31 wd:Q36784.

                    ?commune wdt:P131 ?departement.
                    ?departement wdt:P131 ?region.
                    
                    FILTER (?communePopulation > 25000).
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                    }"""

query_drap = """SELECT DISTINCT ?departementLabel ?drapeau ?code_insee
                WHERE {
                    VALUES ?type {  wd:Q6465 wd:Q202216  }

                    ?departement wdt:P31 ?type;
                    wdt:P2586 ?code_insee;
                    wdt:P41 ?drapeau.

                    FILTER NOT EXISTS { 
                        FILTER(regex(str(?drapeau), "Flag%20of%20France" )).}
                    
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                    }
                        
                    ORDER BY ?code_insee"""

query_lieu = """SELECT DISTINCT ?departementLabel ?lieu ?imagelieu ?code_insee
                    WHERE 
                        {
                        ?departement wdt:P31 wd:Q6465.
                        
                        ?lieu wdt:P31 wd:Q570116;
                        wdt:P2586 ?code_insee;
                        wdt:P18 ?imagelieu;
                        wdt:P131 ?location.
                        
                        ?location wdt:P131 ?departement.
                        
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                        }
                        
                        ORDER BY ?code_insee"""

# Si une query est faite pour chaque question générée
AVAILABLE_QUERIES = {
    'departement': query_gen,
    'commune': query_cmn, 
    'drapeau': query_drap,
    "lieu": query_lieu
}

# Si les queries sont exécutées puis stockées
AVAILABLE_DATAFRAMES = {
    'departement': None,
    'commune': None,
    'drapeau': None,
    'lieu': None
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
    for _ in range(nb_question):
        
        q_type = question_type or random.choice(question_types) or random.choice(AVAILABLE_QUESTION_TYPES.keys())
        q_spec = AVAILABLE_QUESTION_TYPES.keys()
        path_to_dataframe = f'{q_type}.csv'
        
        # On regarde dans la fonction generate_question si la query a déjà été effectuée ou non
        # On ne s'en soucie pas ici du coup
        element, answer_prop, answer, options = handler.generate_question(
            question_attr=q_spec['question_attr'],
            answer_attr=q_spec['answer_attr'],
            query_type=q_spec['query_type'], # FIXME: le plus simple serait de basculer le dict des queries dans le query handler
            # pour ne passer en argument que la clé, pas la longue str de la query
            query=AVAILABLE_QUERIES[q_spec['query_type']] # FIXME: à virer lorsque que la modification du dessus sera faite
        )
        
        # FIXME: Si on veut pouvoir récupérer plusieurs attributs pour la question il faut transformer 'question_attr' en liste d'attributs
        # La méthode generate question devra le traiter en conséquence

        if q_spec['answer_attr'] == answer_prop.removesuffix('.value'): # FIXME: cette vérif peut maintenant être faite dans le query handler
            to_ask = q_spec['question'].replace('X', element)
            question_list.append(to_ask)
            options.append(answer)
            random.shuffle(options)
            answer_list.append(answer)
            option_list.append(options)

    return question_list, answer_list, option_list
            
        
