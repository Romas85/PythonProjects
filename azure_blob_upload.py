import logging
import azure.functions as func
import os
import requests
from azure.storage.blob import BlobServiceClient
from datetime import datetime

app = func.FunctionApp()

@app.schedule(schedule="0 0 9,14,19 * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_triggernsq(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    
    # failo URL
file_url = 'https://nasdaqbaltic.com/statistics/en/shares?download=1'

# Gauname šiandienos datą kaip eilutę
current_date = datetime.now().strftime("%Y-%m-%d")

# Failo pavadinimas su data
file_name = f"downloaded_shares_{current_date}.csv"

# Azure Blob Storage prisijungimo informacija
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') # Kintamasis
container_name = "nasdaqbaltic" 

# Sukurkite BlobServiceClient objektą
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

# Atsiunčiamas failas
response = requests.get(file_url)


if response.status_code == 200:
    # Įkeliamas failo turinys į Azure Blob
    blob_client.upload_blob(response.content, overwrite=True)
    print(f"Failas '{file_name}' sėkmingai įkeltas į '{container_name}' Azure Blob Storage.")
else:
    print("Nepavyko atsisiųsti failo.")