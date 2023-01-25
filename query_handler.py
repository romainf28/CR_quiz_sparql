import pandas as pd
import random
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import random
from queries import AVAILABLE_QUESTION_TYPES, AVAILABLE_QUERIES


class QueryHandler():
    def __init__(self, url="https://query.wikidata.org/sparql"):
        self.url = url
        self.sparql_wrapper = SPARQLWrapper(url)

    def execute_query(self, query):
        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setReturnFormat(JSON)
        results = self.sparql_wrapper.query().convert()
        df_res = pd.json_normalize(results['results']['bindings'])
        return df_res

    def filter_properties(self, properties):
        return [prop for prop in properties if prop.endswith("value") and prop != "item.value" and prop != "itemLabel.value"]

    # def check_if_url(self, df, candidate, property):
    #     name = list(df[df["item.value"] == candidate]
    #                 ["itemLabel.value"].drop_duplicates())[0]
    #     if '//' in property or '//' in name:
    #         return None
    #     return name

    def select_answer_and_options(self, df, question_type):

        ids = list(df["departement.value"].drop_duplicates())

        question_attr = AVAILABLE_QUESTION_TYPES[question_type]['question_attr']
        answer_prop = AVAILABLE_QUESTION_TYPES[question_type]['answer_attr']
        # properties = self.filter_properties(df.columns)
        # answer_prop = random.choice(properties)

        if len(ids) == 0:
            print("Error")
            exit(0)

        candidate_id = random.choice(ids)
        element = list(df[df["departement.value"] == candidate_id]
                       [f'{question_attr}.value'].drop_duplicates())[0]
        # ids.remove(candidate_id)

        # name = self.check_if_url(df,
        #                          candidate_id,
        #                          answer_prop)

        answer = list(df[df["departement.value"] == candidate_id]
                      [f'{answer_prop}.value'].drop_duplicates())[0]
        options = list(df[df["departement.value"] != candidate_id]
                       [f'{answer_prop}.value'].drop_duplicates())

        return element, answer, random.sample(options, 3)

    def generate_question(self, question_type):
        query_type = AVAILABLE_QUESTION_TYPES[question_type]['query_type']
        if not (os.path.isfile('dataframes/{}.csv'.format(query_type))):
            query = AVAILABLE_QUERIES[query_type]
            res_df = self.execute_query(query)
            res_df.to_csv('dataframes/{}.csv'.format(query_type), index=False)
        else:
            res_df = pd.read_csv('dataframes/{}.csv'.format(query_type))
        return self.select_answer_and_options(res_df, question_type)


handler = QueryHandler()
res_df = handler.execute_query(AVAILABLE_QUERIES['departement'])
res_df.to_csv('results.csv')
