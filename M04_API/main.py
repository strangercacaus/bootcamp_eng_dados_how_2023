import datetime
import time

from schedule import repeat, every, run_pending
from ingestors import DaySummaryIngestor
from writers import DataWriter

if __name__ == "__main__":
    ingestor = DaySummaryIngestor(
        writer=DataWriter,
        coins=['BTC', 'ETH', 'LTC'],
        default_start_date=datetime.date(2021, 6, 1)
    )

    @repeat(every(1).seconds)
    def job():
        ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)