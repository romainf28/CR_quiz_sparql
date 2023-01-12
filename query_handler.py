import pandas as pd
import random
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np

class QueryHandler():
    def __init__(self, url="https://query.wikidata.org/sparql"):
        self.url = url
        self.sparql_wrapper = SPARQLWrapper(url)
        self.limit = 30
        self.query = """SELECT DISTINCT ?departement ?code_INSEE ?departementLabel WHERE 
                        {
                        ?departement wdt:P31 wd:Q6465;
                        wdt:P2586 ?code_INSEE.
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "fr" }
                        }
                        ORDER BY ?code_INSEE"""


    def execute_query(self,query):
        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setReturnFormat(JSON)
        results = self.sparql_wrapper.query().convert()
        df_res = pd.json_normalize(results['results']['bindings'])
        return df_res
