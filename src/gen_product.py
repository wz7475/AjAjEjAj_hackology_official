import pandas as pd
import numpy as np

# Read the shops_data.csv file
df = pd.read_csv('../data/shops_data.csv')

# Select features for transformation
features = ['liczba budynków – suma', 'szacowana liczba mieszkańców razem', 'gęstość zaludnienia osób na km2',
            'szacowany średni wiek mieszkańców razem', 'liczba firm prywatnych',
            'wskaźnik atrakcyjności - średnia wartość dla obszaru chwytania']

# Create a new dataframe for product1
product1 = pd.DataFrame()

# Apply non-linear transformations
product1['sales'] = np.pow(np.log1p(df[features[0]]) * np.sqrt(df[features[1]]), 3)

# Save the new dataframe to product1.csv
product1.to_csv('../data/product4.csv', header=["0"])

print(product1.head())
