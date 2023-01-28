from query_handler import QueryHandler
from cairosvg import svg2png
from PIL import Image
from queries import query_lieu
import requests
from io import BytesIO


handler = QueryHandler()
df_lieux = handler.execute_query(query_lieu)
i = 0
for idx, row in df_lieux.iterrows():
    print(i)
    url = row['imagelieu.value']
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    response = requests.get(url, stream=True, headers=headers)
    print(response.status_code)
    response.raw.decode_content = True
    with open('assets/places/{}.png'.format(row['lieuLabel.value']), 'wb') as outfile:
        outfile.write(response.content)

    i += 1
# df_lieux.to_csv('results.csv')
