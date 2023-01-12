from query_handler import QueryHandler
import pandas as pd

handler = QueryHandler()
df_res = handler.execute_query(handler.query)
df_res.to_csv('results.csv')