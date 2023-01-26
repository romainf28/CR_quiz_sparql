from query_handler import QueryHandler
from cairosvg import svg2png
from PIL import Image
from queries import query_drap
import requests
from io import BytesIO

handler = QueryHandler()
df_flags = handler.execute_query(query_drap)
for idx, row in df_flags.iterrows():

    if not (row['code_insee.value'] in ("2A", "2B")) and int(row['code_insee.value']) >= 82:
        if row['drapeau.value'].endswith('svg'):
            svg2png(url=row['drapeau.value'],
                    write_to='assets/flags/{}.png'.format(row['code_insee.value']))
        if row['drapeau.value'].endswith('gif'):
            url = row['drapeau.value']

            im = Image.open(BytesIO(requests.get(url).content))
            im.save('assets/flags/{}.png'.format(row['code_insee.value']))
