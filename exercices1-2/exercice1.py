import pandas as pd
import requests
from typing import Dict, Any

def find_peak_consumption(file_path: str) -> Dict[str, Any]:
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    df.columns = df.columns.str.strip()

    if 'Date' not in df.columns or 'Valeur (TWh)' not in df.columns:
        raise KeyError("'Date' ou 'Valeur (TWh)' non trouvé dans le fichier CSV")

    # Convertion
    df['Date'] = df['Date'].astype(str).str.strip()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Valeur (TWh)'] = df['Valeur (TWh)'].str.replace(',', '.').astype(float)

    # valeur max
    peak_row = df.loc[df['Valeur (TWh)'].idxmax()]

    # Retourne la date, l'heure et la consommation maximale (ps : l'heure, le jour et le mois ne sont pas disponibles dans le fichier CSV)
    return {
        'date': peak_row['Date'].strftime('%Y-%m-%d %H:%M:%S'),
        'region': peak_row['Region'],
        'consumption_twh': peak_row['Valeur (TWh)']
    }

# dl fichier CSV depuis l'URL fournie
r = requests.get('https://analysesetdonnees.rte-france.com/sites/default/files/graphDownloads/R%25C3%25A9partition_de_la_consommation_d%2527%25C3%25A9lectricit%25C3%25A9_fran%25C3%25A7aise_par_r%25C3%25A9gion_2024-08-14_10-21.csv')
with open('dataExo1.csv', 'wb') as f:
    f.write(r.content)

file_path = 'dataExo1.csv'
result = find_peak_consumption(file_path)

if result:
    print(f"La consommation maximale d'électricité a eu lieu le {result['date']} dans la région {result['region']}.")
    print(f"La consommation était de {result['consumption_twh']} TWh.")

