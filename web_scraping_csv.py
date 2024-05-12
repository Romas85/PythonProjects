import requests
from bs4 import BeautifulSoup
import csv 
from datetime import datetime
 
#Musu web nusirodom
url_address = "https://www.bns.lt/"
visos_naujienos=[]
antrastes= ['Data', 'Kategorija', 'Antraste']
#apgaunu, kad jungiuosi su narsikle
request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    #siunciame uzklausa, kad pasiimtume web
#pasiimam web turini
response = requests.get(url_address, headers=request_headers)

HTML_kodas = BeautifulSoup(response.content, "html.parser")
 
naujienos = HTML_kodas.find_all("div", class_="js-newsline-container")
 
for naujiena in naujienos:
    data=naujiena.find("span", class_="time").text
    kategorija=naujiena.find("span", class_="tag-label").text
    antraste=naujiena.find("div", class_="newsline-container-link").text.replace("\n","")
    visos_naujienos.append([data, kategorija, antraste])
 
#nustatudata, kad panaudociau failo pavadinime
dabar = datetime.now() # dabartinis laikas
date_time = dabar.strftime("%Y-%m-%d %H-%M-%S")  

#sukuriam failo pavadinima
failas= "BNS_naujienos" + date_time + ".csv"
#failo pilna direktorija(path)
vieta="C:/Temp/" + failas

with open(vieta, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(antrastes)
    writer.writerows(visos_naujienos)

print("atspausdinta")