import requests
import pandas as pd

# Jūsų API raktas
api_key = 'e15c5eff52e74abeb9f1216644dbeb92'

# Užklausos URL
url = "https://comtradeapi.un.org/data/v1/get/C/M/HS"

# Užklausos parametrai
params = {
    'reporterCode': '276',  # Vokietijos M49 kodas
    'period': '202312',
    'cmdCode': '681189',  # Produkto kodas
    'flowCode': 'M',  # Importo srautas
    'includeDesc': True,  # Įtraukti aprašymus
    'key': api_key
}

# Atlikite užklausą
response = requests.get(url, params=params)

# Patikrinkite, ar užklausa sėkminga
if response.status_code == 200:
    # Konvertuokite duomenis į DataFrame
    data = response.json().get('data')
    if data:  # Patikriname, ar duomenų masyvas nėra tuščias
        df = pd.DataFrame(data)
        # Grupuojame duomenis pagal 'partnerDesc' ir sumuojame reikiamus stulpelius
        grouped_df = df.groupby('partnerDesc').agg({
            'qty': 'sum',  # Sumuojame kiekį
            'netWgt': 'sum',  # Sumuojame neto svorį
            'cifvalue': 'sum',  # Sumuojame CIF vertę
            'fobvalue': 'sum'  # Sumuojame FOB vertę (jei prieinama)
        }).reset_index()
        
        csv_file_path = 'C:/Temp/comtrade_aggregated_data.csv'  # Failo saugojimo kelias
        grouped_df.to_csv(csv_file_path, index=False)
        print(f"Aggregated data has been written to {csv_file_path}")
    else:
        print("No data available in the response.")
else:
    print("Failed to retrieve data:", response.status_code, response.text)
