import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/?pagina={}'

i = 1
ret = requests.get(url.format(i))
ret
soup = bs(ret.text, features="html5lib")
soup
houses = soup.find_all('article',{'class':'property-card__container js-property-card'})

house = houses[0]

descricao = house.find('span',{'class':'js-card-title'}).text.strip()
endereço = house.find('span',{'class':'property_card__address'}).text.strip()
valor = house.find('div',{'class':'property_card__price'}).text.strip()
condomínio = house.find('strong',{'class':'js-condo-price'}).text.strip()
area = house.find('span',{'class':'js-card-title'}).text.strip()
qtd banheiros = house.find('span',{'class':'js-card-title'}).text.strip()
qtd_quartos = house.find('span',{'class':'js-card-title'}).text.strip()
qtd_vagas = house.find('span',{'class':'js-card-title'}).text.strip()
piscina = house.find('span',{'class':'js-card-title'}).text.strip()
link = house.find('span',{'class':'js-card-title'}).text.strip()