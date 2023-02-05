# Importando os Módulos Necessários

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Definindo a URL da página a ser capturada, com um placeholder para a iteração de páginas.

url = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/?pagina={}'

# Gerando uma requisição para retornar a quantidade total de anúncios disponíveis:

ret = requests.get(url.format(1))
soup = bs(ret.text, features="html5lib")
houses_num = int(soup.find('strong',{'class':'results-summary__count'}).text.strip().replace('.',''))

# Criando o DataFrame

df = pd.DataFrame(
    columns=['descricao','endereco','valor','condominio','area','qtd_banheiros','qtd_quartos'
             ,'qtd_vagas','wlink'
             ]
)

# Zerando a Variável de Controle:

i = 1

# Criando o Loop para iterar por todas as páginas até concluir a extração de todos os anúncios

while df.shape[0] < houses_num:
    # Mesma requisição de antes, porém retornando todas as tags article
    ret = requests.get(url.format(i))
    soup = bs(ret.text, features="html5lib")
    houses = soup.find_all('article', {'class': 'property-card__container js-property-card'})
    # Loop, itera todas as tags article tentando encontrar a tag correspondente ao valor desejado, se não encontra, define None 
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
        
        # Define uma lista com o valor das variáveis acima e guarda na última posição do dataframe.
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
    # Atualiza a variável de controle e printa o status da execução do loop
    i += 1
    print(f'i = {i} \t \tsize = {df.shape[0]}')

# Printa o formato final do dataframe
print(df.shape)

# Salva um arquivo com o DataFrame.
df.to_csv('/M02_fundamentos_ingestao/banco_de_imoveis.csv',sep = ',', index = False)