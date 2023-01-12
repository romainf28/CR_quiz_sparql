import pandas as pd
import random
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import random

class QueryHandler():
    def __init__(self, url="https://query.wikidata.org/sparql"):
        self.url = url
        self.sparql_wrapper = SPARQLWrapper(url)
        self.limit = 30
        self.query = """SELECT DISTINCT ?item ?code_insee ?itemLabel WHERE 
                        {
                        ?item wdt:P31 wd:Q6465;
                        wdt:P2586 ?code_insee.
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                        }
                        ORDER BY ?code_insee"""


    def execute_query(self,query):
        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setReturnFormat(JSON)
        results = self.sparql_wrapper.query().convert()
        df_res = pd.json_normalize(results['results']['bindings'])
        return df_res

    def filter_properties(self,properties):
        return [prop for prop in properties if prop.endswith("value") and prop != "item.value" and prop!="itemLabel.value"]

    def check_if_url(self,df,candidate,property):
        name = list(df[df["item.value"] == candidate]["itemLabel.value"].drop_duplicates())[0]
        if '//' in property or '//' in name :
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
        answer = list(df[df["item.value"] == candidate_id][answer_prop].drop_duplicates())[0]
        options = list(df[df["item.value"] != candidate_id][answer_prop].drop_duplicates())
        random.shuffle(options)
        return name, answer_prop, answer,options[:3]

    def generate_question(self):
        res_df = self.execute_query(self.query)
        return self.select_answer_and_options(res_df)