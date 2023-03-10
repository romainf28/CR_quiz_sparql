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
        'answer_attr': 'departementPopulation',
        'query_type': 'departement',
        'question': 'Quelle est la population du département X ?'
    },
    'dpt_surface': {
        'question_attr': 'departementLabel',
        'answer_attr': 'Area',
        'query_type': 'departement',
        'question': 'Quelle est la surface du département X en km^2 ?'
    },
    'code_drapeau': {
        'question_attr': 'departementLabel',
        'answer_attr': 'code_insee',
        'query_type': 'drapeau',
        'question': 'Quel est le drapeau du département X ?',
        'image': True
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
        'answer_attr': 'code_commune',
        'query_type': 'commune',
        'question': 'Quel est le code postal de la commune X ?'
    },
    'code_cmn': {
        'question_attr': 'code_commune',
        'answer_attr': 'communeLabel',
        'query_type': 'commune',
        'question': 'Quelle commune correspond au code postal X ?'
    },
    'lieu_dpt': {
        'question_attr': 'lieuLabel',
        'answer_attr': 'departementLabel',
        'query_type': 'lieu',
        'question': 'Dans quel département se situe le lieu X ?'
    },
    'dpt_lieu': {
        'question_attr': 'departementLabel',
        'answer_attr': 'lieuLabel',
        'query_type': 'lieu',
        'question': 'Lequel de ces lieux se situe dans le département X ?',
        'image': True

    }
}

query_gen = """SELECT DISTINCT ?departement ?code_insee ?departementLabel ?drapeau ?Area ?capitaleLabel ?departementPopulation ?regionLabel

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
            SELECT DISTINCT ?departement ?departementLabel ?communeLabel ?communePopulation ?code_commune ?regionLabel ?code_insee
            WHERE {
                {
                    SELECT (?commune as ?departement) (?communeLabel as ?departementLabel) ?communeLabel ?communePopulation ?code_commune ?regionLabel ?code_insee
                    WHERE {
                        ?commune wdt:P31 wd:Q5119 .
                        ?commune wdt:P17 wd:Q142 ;
                        wdt:P1082 ?communePopulation;
                        wdt:P2586 ?code_insee;
                        wdt:P281 ?code_commune.
                        ?metropole wdt:P31 wd:Q3333855 .
                        ?region wdt:P31 wd:Q36784 .

                        ?metropole  wdt:P131 ?region .
                        SERVICE wikibase:label {bd:serviceParam wikibase:language "fr" .}
                    }
                }
                UNION
                {
                    SELECT DISTINCT ?departement ?departementLabel ?communeLabel ?communePopulation ?code_commune ?regionLabel ?code_insee
                    WHERE {
                        VALUES ?type {  wd:Q6465 wd:Q202216  }

                        ?departement wdt:P31 ?type;
                        wdt:P2586 ?code_insee.

                        ?commune wdt:P31 wd:Q484170;
                        wdt:P1082 ?communePopulation;
                        wdt:P281 ?code_commune.
                        ?region wdt:P31 wd:Q36784.
                        ?commune wdt:P131 ?departement.
                        ?departement wdt:P131 ?region.
                        FILTER (?communePopulation > 25000).
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                    }
                }
            }

                
"""

query_drap = """SELECT DISTINCT ?departement ?departementLabel ?drapeau ?code_insee
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

query_lieu = """
            SELECT DISTINCT ?departement ?departementLabel ?lieu ?lieuLabel ?imagelieu ?code_insee WHERE 
            {
                {
                    SELECT DISTINCT ?departement ?departementLabel ?lieu ?lieuLabel ?imagelieu ?code_insee
                    WHERE 
                        {
                        ?departement wdt:P31 wd:Q6465;
                        wdt:P2586 ?code_insee.
                        
                        ?lieu wdt:P31 wd:Q570116;
                        wdt:P18 ?imagelieu;
                        wdt:P131 ?location.
                        
                        ?location wdt:P131 ?departement.
                        
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                        }
                        
                        ORDER BY ?code_insee
                }

                UNION

                {
                    SELECT DISTINCT (?city as ?departement) (?cityLabel as ?departementLabel) ?lieu ?lieuLabel ?imagelieu ?code_insee
                    WHERE 
                        {
                        ?arrondissement wdt:P31 wd:Q702842.

                        ?city wdt:P31 wd:Q5119 .
                        ?city wdt:P17 wd:Q142 ;
                        wdt:P2586 ?code_insee;
                        rdfs:label ?cityLabel.
                        FILTER (lang(?cityLabel) = "fr").
                        
                        ?lieu wdt:P31 wd:Q570116;
                        wdt:P18 ?imagelieu;
                        wdt:P131 ?location.
                        
                        ?location wdt:P131 ?arrondissement.
                        ?arrondissement wdt:P131 ?city
                        
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr"}
                        
                        }
                        
                        ORDER BY ?code_insee
                }

            }
"""


# Si une query est faite pour chaque question générée
AVAILABLE_QUERIES = {
    'departement': query_gen,
    'commune': query_cmn,
    'drapeau': query_drap,
    "lieu": query_lieu
}
