import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/?pagina={}'

ret = requests.get(url.format(1))
soup = bs(ret.text, features="html5lib")
qtd_casas = int(soup.find('strong',{'class':'results-summary__count'}).text.strip().replace('.',''))

df = pd.DataFrame(
    columns=['descricao','endereco','valor','condominio','area','qtd_banheiros','qtd_quartos'
             ,'qtd_vagas','wlink'
             ]
)

i = 1

while i < 50:
    ret = requests.get(url.format(i))
    soup = bs(ret.text, features="html5lib")
    houses = soup.find_all('article', {'class': 'property-card__container js-property-card'})
    for house in houses:
        try:
            descricao = house.find('span', {'class': 'js-card-title'}).text.strip()
        except:
            descricao = None
        try:
            endereco = house.find('span', {'class': 'property_card__address'}).text.strip()
        except:
            endereco = None
        try:
            valor = house.find('div', {'class': 'property-card__price'}).text.strip()
        except:
            valor = None
        try:
            condominio = house.find('strong', {'class': 'js-condo-price'}).text.strip()
        except:
            condominio = None
        try:
            area = house.find('span', {'class': 'js-property-card-detail-area'}).text.strip()
        except:
            area = None
        try:
            qtd_banheiros = house.find('li', {'class': 'property-card__detail-bathroom'}).text.strip()
        except:
            qtd_banheiros = None
        try:
            qtd_quartos = house.find('li', {'class': 'property-card__detail-room'}).text.strip()
        except:
            qtd_quartos = None
        try:
            qtd_vagas = house.find('li', {'class': 'property-card__detail-garage'}).text.strip()
        except:
            qtd_vagas = None
        try:
            wlink = 'https://vivareal.com.br' + house.find('a', {'class': 'property-card__labels-container'})['href']
        except:
            wlink = None

        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            valor,
            condominio,
            area,
            qtd_banheiros,
            qtd_quartos,
            qtd_vagas,
            wlink
        ]
    i += 1
    print(f'i = {i} \t \tsize = {df.shape[0]}')

print(df.shape)

df.to_csv('banco_de_imoveis.csv',sep = ',', index = False)