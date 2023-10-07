import sys
import datetime
import pytest
sys.path.append('M04_API')
from apis import DaySummaryApi, TradesAPI

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