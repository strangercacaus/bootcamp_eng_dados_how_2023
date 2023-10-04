import datetime
import json
import os
from typing import List

from ingestors import DataTypeNotSupportedForIngestionException


class DataWriter():

    def __init__(self, coin: str, api:str) -> None:
        self.api=api
        self.coin=coin
        self.filename = f'M04_API/{self.api}/{self.coin}/{datetime.datetime.now()}.json'

    def _write_row(self, row:'str') ->None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a") as f:
            f.write(row)

    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)
