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
        self.query = """
        SELECT DISTINCT ?country ?countryLabel ?capital ?capitalLabel
        WHERE
        {
        ?country wdt:P31 wd:Q3624078 .
        #not a former country
        FILTER NOT EXISTS {?country wdt:P31 wd:Q3024240}
        #and no an ancient civilisation (needed to exclude ancient Egypt)
        FILTER NOT EXISTS {?country wdt:P31 wd:Q28171280}
        OPTIONAL { ?country wdt:P36 ?capital } .

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
        }
        ORDER BY ?countryLabel
        """

    def execute_query(self,query):
        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setReturnFormat(JSON)
        results = self.sparql_wrapper.query().convert()
        df_res = pd.json_normalize(results['results']['bindings'])
        return df_res
