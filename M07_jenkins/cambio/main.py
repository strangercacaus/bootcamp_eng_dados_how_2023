import requests
import json
from datetime import date, datetime

def get_cotacao():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url)
    dolar = json.loads(response.text)["USDBRL"]
    return float(dolar["bid"])

with open("cambio/cambio.csv", "a") as file:
    file.write(
        f"{datetime.strftime(datetime.now(),'%d/%m/%y %H:%M')}:{get_cotacao():.2f}\n"
    )