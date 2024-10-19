import pandas as pd

if __name__ == "__main__":
    file_to_fix = "../data/augmented_data_noise.json"
    df = pd.read_json(file_to_fix, orient='columns')
    for index, row in df.iterrows():
        procent_woman = row['populacja - procent kobiet']
        procent_men = row['populacja - procent mężczyzn']
    
        total = procent_woman + procent_men
        scaled_woman = (procent_woman / total) * 100
        scaled_men = (procent_men / total) * 100
        df.at[index, 'populacja - procent kobiet'] = scaled_woman
        df.at[index, 'populacja - procent mężczyzn'] = scaled_men

        population_to_adjust = [
            'populacja - procentowe kategorie wiekowe od 5 do 9 lat',
            'populacja - kategorie wiekowe od 10 do 14 lat',
            'populacja - procentowe kategorie wiekowe od 15 do 19 lat',
            'populacja - procentowe kategorie wiekowe od 20 do 24 lat',
            'populacja - procentowe kategorie wiekowe od 25 do 29 lat',
            'populacja - procentowe kategorie wiekowe od 30 do 34 lat',
            'populacja - kategorie wiekowe od 35 do 39 lat',
            'populacja - procentowe kategorie wiekowe od 40 do 44 lat',
            'populacja - procentowe kategorie wiekowe od 45 do 49 lat',
            'populacja - procentowe kategorie wiekowe od 50 do 54 lat',
            'populacja - procentowe kategorie wiekowe od 55 do 59 lat',
            'populacja - procentowe kategorie wiekowe od 60 do 64 lat',
            'populacja - procentowe kategorie wiekowe od 65 do 69 lat',
            'populacja - procent kategorii wiekowych od 70 do 75 lat',
            'populacja - procent kategorii wiekowych powyżej 75 lat'
        ]
        total = sum([row[p] for p in population_to_adjust])
        
        for p in population_to_adjust:
            df.at[index, p] = (row[p] / total) * 100
        
        for col in df.columns:
            if 'liczba' in col or 'odległość' in col:
                df.at[index, col] = float(int(row[col]))

    # Optionally, save the JSON data to a file
    with open(file_to_fix, 'w', encoding="utf-8") as file:
        file.write(df.to_json(orient='records'))
