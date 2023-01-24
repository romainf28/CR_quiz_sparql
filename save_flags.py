from query_handler import QueryHandler
from cairosvg import svg2png
from PIL import Image


flags_query = """SELECT DISTINCT ?item ?code_insee ?itemLabel ?drapeau WHERE 
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

handler = QueryHandler()
df_flags = handler.execute_query(flags_query)
for idx, row in df_flags.iterrows():
    print(row['code_insee.value'])
    if row['drapeau.value'].endswith('svg'):
        svg2png(url=row['drapeau.value'],
                write_to='assets/flags/{}.png'.format(row['code_insee.value']))
