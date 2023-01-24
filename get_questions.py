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
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    'code_dpt': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    'dpt_capitale': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    }, 
    'dpt_population': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    #'population_dpt',
    'dpt_surface': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    'dpt_drapeau': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    #'surface_dpt', 
    'cmn_region': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    }, 
    'cmn_dpt': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    'cmn_population': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    #'population_cmn',
    'cmn_code': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
    },
    'code_cmn': {
        'answer_attr': 'code_insee.value',
        'query_type': 'departement',
        'question': 'Quel est le numéro du département nommé X ?'
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
                    }
            """


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
    "lieu":query_lieu
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
