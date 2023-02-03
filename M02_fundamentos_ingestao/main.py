# Importando os Módulos:
import requests
import json

# Definindo a URL para a requisição GET:
url = 'https://economia.awesomeapi.com.br/last/USD-BRL'
ret = requests.get(url)

# Checando a validade do retorno da requisição:
# No pacote requests, é possível utilizar o próprio objeto do retorno da requisição como um booleano
# atestando o sucesso, no caso, o código 200 equivale ao valor True.
if ret:
    print(ret)
else:
    print('Falhou')

# Exibindo o resultado:

# Acessando o objeto contendo os valores
dolar = json.loads(ret.text)['USDBRL']

# Formatando a string
print(f"20 Dólares hoje custam {float(dolar['bid']) * 20} reais")


# Definindo no formato de função:
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-', '')]
    print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor}")

# Implementando um tratamento de erros
# Estrutura básica com 'try'

try:
    cotacao(50, 'Cavalo')
except Exception as e:
    print(e)
else:
    print('Ok')

# Definindo uma lista de moedas com um erro ("RPL-BRL")

lst_money = [
    "USD-BRL",
    "EUR-BRL",
    "BTC-BRL",
    "JPY-BRL",
    "RPL-BRL"
]

valor = 20

# Criando uma estrutura com identificação de erro

for moeda in lst_money:
    try:
        url = f'https://economia.awesomeapi.com.br/last/{moeda}'
        ret = requests.get(url)
        dolar = json.loads(ret.text)[moeda.replace('-', '')]
        print(f"{valor} {moeda[:3] } hoje custam {float(dolar['bid']) * valor} {moeda[0:3]}")
    except:
        print(f'Falha na moeda {moeda}')

# Incorporando o try na função anterior

def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    try:
        ret = requests.get(url)
        dolar = json.loads(ret.text)[moeda.replace('-', '')]
        print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor}")
    except:
        print(f'Falha na moeda {moeda}')

# Chamando a função:

for coin in lst_money:
    cotacao(20, coin)

# Criando um decorador
def error_check(func):
    def inner_func(*args,**kwargs):
        try:
            func(*args, **kwargs)
        except:
            f'{func.__name__} falhou.'
    return inner_func

# Aplicando decorador na função:

@error_check
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'
    try:
        ret = requests.get(url)
        dolar = json.loads(ret.text)[moeda.replace('-', '')]
        print(f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor}")
    except:
        print(f'Falha na moeda {moeda}')

#Refazendo a chamada:

for coin in lst_money:
    cotacao(20, coin)

# Utilizando o pacote Back-Off
import backoff
import random

@backoff.on_exception(backoff.expo,(ConnectionRefusedError,ConnectionAbortedError,TimeoutError),max_tries = 10)
def test_func(*args, **kwargs):
    rnd = random.random()
    print (f"""
           RND: {rnd}
           args: {args if args else 'no args'}
           kwargs: {kwargs if kwargs else 'no kwargs'}
           """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise TimeoutError('Tempo de espera excedido')
    else:
        return "OK!"

test_func(42, 51, nome = "Cauê")