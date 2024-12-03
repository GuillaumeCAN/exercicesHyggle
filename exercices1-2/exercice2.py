from typing import List
import pandas as pd
import re
import requests

def custom_sort(strings: List[str]) -> List[str]:
    return sorted(strings, key=lambda x: (len(x), x.lower()))

r = requests.get('https://www.data.gouv.fr/fr/datasets/r/4c176588-a444-4dc7-b6bf-60390ae7e5be')
file_path = 'dataExo2.csv'
with open(file_path, 'wb') as f:
    f.write(r.content)

df = pd.read_csv(file_path, sep=";", encoding="utf-8", header=1)
df.columns = df.columns.str.strip()

df['Typologie des données impactées'] = df['Typologie des données impactées'].astype(str).str.strip()

# valeurs uniques de la colonne + tri
typoDonneesImpactees = df['Typologie des données impactées'].dropna().unique().tolist()
sorted_typologies = custom_sort(typoDonneesImpactees)

def remove_parentheses(strings):
    return [re.sub(r'\([^)]*\)', '', s) for s in strings]

sorted_typologies = remove_parentheses(sorted_typologies)
sorted_typologies = list(set(s for s in sorted_typologies if s.lower() != 'nan'))
print(sorted_typologies)