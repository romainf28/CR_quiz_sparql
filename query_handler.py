import requests
import pandas as pd
import random
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import random
from os.path import exists

class QueryHandler():
    def __init__(self, url="https://query.wikidata.org/sparql"):
        self.url = url
        self.sparql_wrapper = SPARQLWrapper(url)
        self.limit = 30
        self.query = """SELECT DISTINCT ?item ?code_insee ?itemLabel ?drapeau WHERE 
                        {
                        VALUES ?type {  wd:Q6465 wd:Q202216  }
                        ?item wdt:P31 ?type;
                        wdt:P2586 ?code_insee;
                        wdt:P41 ?drapeau.
                        FILTER NOT EXISTS { 
                            FILTER(regex(str(?drapeau), "Flag%20of%20France" )) . 
                        }
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                        }
                        ORDER BY ?code_insee"""

    def execute_query(self, query):
        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setReturnFormat(JSON)
        results = self.sparql_wrapper.query().convert()
        df_res = pd.json_normalize(results['results']['bindings'])
        return df_res

    def filter_properties(self, properties):
        return [prop for prop in properties if prop.endswith("value") and prop != "item.value" and prop != "itemLabel.value"]

    def check_if_url(self, df, candidate, property):
        name = list(df[df["item.value"] == candidate]
                    ["itemLabel.value"].drop_duplicates())[0]
        if '//' in property or '//' in name:
            return None
        return name

    def select_answer_and_options(self, df):
        ids = list(df["item.value"].drop_duplicates())
        selected = False
        properties = self.filter_properties(df.columns)
        answer_prop = random.choice(properties)
        while not selected:
            if len(ids) == 0:
                print("Error")
                exit(0)

            candidate_id = random.choice(ids)
            ids.remove(candidate_id)

            name = self.check_if_url(df,
                                     candidate_id,
                                     answer_prop)
            if name:
                selected = True
        answer = list(df[df["item.value"] == candidate_id]
                      [answer_prop].drop_duplicates())[0]
        options = list(df[df["item.value"] != candidate_id]
                       [answer_prop].drop_duplicates())
        random.shuffle(options)
        return name, answer_prop, answer, options[:3]

    def generate_question(self):
        res_df = self.execute_query(self.query)
        return self.select_answer_and_options(res_df)
    
    def check_if_url_v2(self, df, candidate, question_attr, answer_attr):
        name = list(df[df[f"{question_attr}.value"] == candidate])[0]
                    #["itemLabel.value"].drop_duplicates())[0]
        return name
    
    def select_answer_and_options_v2(self, question_attr, answer_attr, query_type):
        """Sélectionne les éléments nécessaires à la création d'une question du type demandé dans le dataframe résultant de la requête SparQL.
        
        *param question_attr* str: nom de la colonne du df dans laquelle choisir un sujet pour la question
        *param answer_attr* str: nom de la colonne du df dans laquelle choisir la bonne et les mauvaises réponses à la question
        *param query_type* str: à valeur dans ['departement', 'commune', 'drapeau', 'lieu']
        """
        ids = list(df[f"{question_attr}.value"].drop_duplicates())
        selected = False
        while not selected:
            if len(ids) == 0:
                print("Error")
                exit(0)

            candidate_id = random.choice(ids)
            ids.remove(candidate_id)

            name = self.check_if_url_v2(df,
                candidate_id,
                question_attr,
                answer_attr)
            if name:
                selected = True
        answer = list(df[df[f"{question_attr}.value"] == candidate_id]
                      [answer_attr].drop_duplicates())[0]
        options = list(df[df[f"{question_attr}.value"] != candidate_id]
                       [answer_attr].drop_duplicates())
        random.sample(options, 3)
        return name, answer_prop, answer, options
    
    def generate_question_v2(self, question_attr, answer_attr, query_type, query):
        """Vérifie si le résultat de la query existe déjà, sinon exécute la query."""
        eventual_df_path = f'.\\query_results\\{query_type}.csv'
        if exists():
            result_df = pd.read_csv(eventual_df_path)
        else:
            result_df = self.execute_query(query)
        return self.select_answer_and_options_v2(question_attr, answer_attr, query_type, query)
        


handler = QueryHandler()
df_res = handler.execute_query(handler.query)
df_res.to_csv('results.csv')
