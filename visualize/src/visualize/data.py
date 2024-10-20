import pandas as pd
from random import random


def gen_data():
	return {
	'age': {
		'5-9': random(),
		'15-19': random(),
		'30-35': random(),
		'70+': random()
	},
	'sex': {
		'm': random(),
		'f': random()
	},
	'poi': {
		'churches': random(),
		'univeristy': random(),
		'shop': random(),
		'pub': random()
	},
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