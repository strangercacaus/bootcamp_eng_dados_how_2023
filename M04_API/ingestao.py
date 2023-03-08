from ast import List
import requests
import logging
from abc import ABC, abstractmethod
import datetime
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi():

    def __init__(self, coin:str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    def get_data(self,**kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f'Gettning data from endpoint {endpoint}')
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
class DaySummaryAPI(MercadoBitcoinApi):
    type = 'day-summary'

    def _get_endpoint(self, date: datetime.date) -> str:
        return f'{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}'

response = DaySummaryAPI(coin='BTC').get_data(date= datetime.date(2023,3,5))

class TradesAPI(MercadoBitcoinApi):
    type = 'trades'

    def _get_unix_epoch(self, date:datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from:datetime.datetime = None, date_to:datetime.datetime = None) -> str:
        
        if date_from and not date_to:
            unix_from = self._get_unix_epoch(date_from)
            return f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_from}'
        
        if date_from and date_to:
            unix_from = self._get_unix_epoch(date_from)
            unix_to = self._get_unix_epoch(date_to)
            return f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_from}/{unix_to}'
        
        else:
            return f'{self.base_endpoint}/{self.coin}/{self.type}'
        
class DataTypeNotSupportedForIngestionException(Exception):

    def __init__(self, data):
        self.data = data
        self.message = f'Data type {type(data)} is not supported for ingestion'
        super().__init__(self.message)

class DataWriter():

    def __init__(self, filename:str) -> None:
        self.filename = filename
    
    def _write_row(self, row:'str') ->None:
        with open(self.filename, "a") as f:
            f.write(row)

    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data,list):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)

response2 = TradesAPI(coin='BTC').get_data(date_from=datetime.datetime(2023,3,1))


data = TradesAPI("BTC").get_data()
writer = DataWriter('trades.json')
writer.write(data)



