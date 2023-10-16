import datetime

from M04_API.code.apis import DaySummaryApi

class TestDaySummaryApi:
    def test_get_data(self):
        """"
        Testa a integração GET da DaySummaryApi retornando o valor 'Date'

        Teste de integração do tipo black box que chama o método get_data para a classe DaySummaryApi e avalia o retorno de um json adequado.
        """
        actual = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2021,1,6))
        expected = {
                    'date': '2021-01-06',
                    'opening': 179000,
                    'closing': 198003.00001,
                    'lowest': 178000.78274,
                    'highest': 200000,
                    'volume': '98696247.74354485', 
                    'quantity': '519.02626054', 
                    'amount': 39513, 
                    'avg_price': 190156.55901294
                    }
        assert actual == expected

    def test_get_data_better(self):
        """"
        Testa a integração GET da DaySummaryApi retornando o valor 'Date'

        Teste de integração do tipo black box que chama o método get_data para a classe DaySummaryApi e avalia o retorno do valor 'date'.
        """
        actual = DaySummaryApi(coin='BTC').get_data(date=datetime.date(2021,1,6)).get("date")
        expected = '2021-01-06'
        assert actual == expected