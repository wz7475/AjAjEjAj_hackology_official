import requests
import pandas as pd
from tqdm import tqdm


df = pd.read_csv('cooridinates.csv', index_col=0, header=0)

values = list()

for x, val in tqdm(df[2873:].iterrows()):
    lat, lon = val[0], val[1]
    r = requests.get(f'https://api.locit.dev.beecommerce.pl/catchment_area/time/pedestrian/600/{lat}/{lon}/wed%2013:00')
    
    geom = r.json()

    obj = {
        'geom': geom['data']['isolines'][0]['ewkt'],
        'x': lon,
        'y': lat
    }

    header = {'Host': 'api.locit.dev.beecommerce.pl',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Referer': 'http://locit.io/',
    'Content-Type': 'application/json',
    'Origin': 'http://locit.io',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=4'}


    r = requests.post('https://api.locit.dev.beecommerce.pl/catchment_data', 
                json=obj, headers=header)
    print(x, r.text)

    pd.DataFrame(r.json()).to_json(f'{lat}_{lon}.json')

    