import sys
import pytest
import datetime
import requests 

from unittest.mock import patch

sys.path.append('M04_API')

from apis import DaySummaryApi, TradesAPI, MercadoBitcoinApi

class TestDaySummaryApi:
    @pytest.mark.parametrize(
            "coin, date, expected",
            [
                ('BTC',datetime.date(2021,6,21),"https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21"),
                ('ETH',datetime.date(2021,6,21),"https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/21"),
                ('ETH',datetime.date(2021,1,2),"https://www.mercadobitcoin.net/api/ETH/day-summary/2021/1/2")
            ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin=coin)
        actual = api._get_endpoint(date=date)
        assert actual == expected

class TestTradesApi:
    @pytest.mark.parametrize(
            "coin, date_from, date_to, expected",
            [
                ('TESTE',datetime.datetime(2019,1,1), datetime.datetime(2019,1,1,0,0,5), "https://www.mercadobitcoin.net/api/TESTE/trades/1546308000/1546308005"),
                ('TESTE',datetime.datetime(2019,1,1), None, "https://www.mercadobitcoin.net/api/TESTE/trades/1546308000"),
                ('TESTE', None, datetime.datetime(2019,1,1,0,0,5), "https://www.mercadobitcoin.net/api/TESTE/trades"),
                ('TESTE', None, None, "https://www.mercadobitcoin.net/api/TESTE/trades"),
            ]
    )

    def test_get_endpoint(self, coin, date_from, date_to, expected):
        actual = TradesAPI(coin=coin)._get_endpoint(date_from=date_from, date_to=date_to)
        assert actual == expected

    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):
            actual = TradesAPI(coin='TESTE')._get_endpoint(
                date_from=datetime.datetime(2019,1,1,0,0,10),
                date_to=datetime.datetime(2019,1,1,0,0,5)
                )
    
    @pytest.mark.parametrize(
        "date, expected",
        [
            (datetime.datetime(2019,1,1), 1546308000),
            (datetime.datetime(2019,1,1,0,0,5), 1546308005)
        ]
    )
    def test_get_unix_epoch(self, date, expected):
        actual = TradesAPI(coin = 'TEST')._get_unix_epoch(date=date)
        assert actual == expected

@pytest.fixture()
@patch("apis.MercadoBitcoinApi.__abstractmethods__", set())
def fixture_mercado_bitcoin_api():
    return MercadoBitcoinApi(
            coin='TEST'
        )

def mocked_requests_get(*args, **kwargs):
    class MockResponse(requests.Response):

        def __init__(self, json_data, status_code):
            super().__init__()
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data
        
        def raise_for_status(self) -> Exception:
            if self.status_code != 200:
                raise(Exception)
        
    if args[0] == "valid_endpoint":
        return MockResponse(json_data={"foo":"bar"}, status_code=200)
    else:
        return MockResponse(json_data= None, status_code = 404)

class TestMercadoBitcoinApi:
    @patch("requests.get")
    @patch("apis.MercadoBitcoinApi._get_endpoint", return_value= "valid_endpoint")
    def test_get_data_request_called(self,
                                     mock_get_endpoint,
                                     mock_requests,
                                     fixture_mercado_bitcoin_api):
        fixture_mercado_bitcoin_api.get_data()
        mock_requests.assert_called_once_with("valid_endpoint")


    @patch("requests.get", side_effect = mocked_requests_get)
    @patch("apis.MercadoBitcoinApi._get_endpoint", return_value= "valid_endpoint")
    def test_get_data_with_valid_endpoint(self, 
                                          mock_get_endpoint,
                                          mock_requests,
                                          fixture_mercado_bitcoin_api):
        actual = fixture_mercado_bitcoin_api.get_data()
        expected = {"foo":"bar"}
        assert actual == expected

    @patch("requests.get", side_effect = mocked_requests_get)
    @patch("apis.MercadoBitcoinApi._get_endpoint", return_value= "invalid_endpoint")
    def test_get_data_with_invalid_endpoint(self, 
                                          mock_get_endpoint,
                                          mock_requests,
                                          fixture_mercado_bitcoin_api):
        with pytest.raises(Exception):
            fixture_mercado_bitcoin_api.get_data()
