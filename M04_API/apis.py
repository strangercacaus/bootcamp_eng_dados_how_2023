import datetime
from abc import ABC, abstractmethod

import logging
import ratelimit
import requests
from backoff import on_exception, expo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MercadoBitcoinApi():

    def __init__(self, coin:str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'

    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass

    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self,**kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f'Gettinng data from endpoint {endpoint}')
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()


class DaySummaryApi(MercadoBitcoinApi):
    type = "day-summary"

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


class TradesAPI(MercadoBitcoinApi):
    type = 'trades'

    def _get_unix_epoch(self, date:datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from:datetime.datetime = None, date_to:datetime.datetime = None) -> str:
        # sourcery skip: remove-redundant-if
        
        if date_from and not date_to:
            unix_from = self._get_unix_epoch(date_from)
            return f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_from}'

        if date_from and date_to:
            if date_from > date_to:
                raise RuntimeError('Interval start cannot be greater than interval end.')
            unix_from = self._get_unix_epoch(date_from)
            unix_to = self._get_unix_epoch(date_to)
            return f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_from}/{unix_to}'

        else:
            return f'{self.base_endpoint}/{self.coin}/{self.type}'