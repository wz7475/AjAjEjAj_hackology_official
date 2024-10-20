import pandas as pd
from random import random
import json

AGE_KEYS = ['5 do 9', '10 do 14', '15 do 19', '20 do 24', '25 do 29', '30 do 34', '35 do 39', '40 do 44', '45 do 49', '50 do 54', '55 do 59', '60 do 64', '65 do 69', '70 do 75', 'powyżej 75']
POI_KEYS = ['wykształcenie wyższe / uniwersytet', 'rozrywka i kult', 'suma zdrowia', 'szkoła średnia']
def sanitize(text: str):
	return (text
			.replace('populacja - procentowe kategorie wiekowe od ', '')
			.replace(' lat', '')
			.replace('populacja - kategorie wiekowe od ', '')
			.replace('populacja - procent kategorii wiekowych od ', '')
			.replace('populacja - procent kategorii wiekowych ', '')
			.replace('liczba punktów ', '')
			.replace('odległość w metrach do najbliższego POI (-1 = większy niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego POI (-1 = większa niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego POI (-1 = większy niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego POI (-1 = więcej niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego punktu POI (-1 = większy niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego POI (-1 = większy niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego punktu POI (-1 = większa niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego POI (-1 = większe niż 5000 m) - ', '')
			.replace('odległość w metrach do najbliższego punktu POI (-1 = większa niż 5000 m) - ', '')
			)


def gen_data():
	with open('../data/ficzurs_koefiszietns.json', 'r') as fh:
		res: dict[str, str] = json.load(fh)
	df=pd.DataFrame(pd.DataFrame(list({sanitize(k): v for k,v in res.items()}.items()), columns=['key', 'val']), index=range(len(res))).dropna()
	age_df_filer=df['key'].str.contains(r'^\d+ do \d+$|powyżej \d+', regex=True)
	po_df_filter=df['key'].str.contains(r'POI', regex=True)
	poi = df[po_df_filter].copy()
	poi['key']=poi['key'].str.replace('POI - ', '')
	return {
	'age': df[age_df_filer].set_index('key').to_dict()['val'],
	'sex': {
		'm': random(),
		'f': random()
	},
	'poi': poi[poi['key'].isin(POI_KEYS)].set_index('key').to_dict()['val'],
	'localization_type': {
		'city': random(),
		'town': random(),
		'city-town': random(),
	}
}

DATA = {
	'Juice': gen_data(),
	'Apples': gen_data(),
	'Snackbar': gen_data()
}

def get_data_as_df(data: dict)->pd.DataFrame:
	long_data = []
	for category, subcategories in data.items():
		for subcategory, value in subcategories.items():
			long_data.append([category, subcategory, value])
	return pd.DataFrame(long_data, columns=['category', 'subcategory', 'value'])

def get_max_value_keys(data: pd.DataFrame)->dict[str, str]:
	max_value_keys = {}
	for category, values in data.items():
		max_key = max(values, key=values.get)  # Get the key with the maximum value
		max_value_keys[str(category)] = max_key
	return max_value_keys