
from ingestors import DataIngestor

class TestDataIngestors:
    def test_checkpoint_filename(self):
        actual = DataIngestor(
            writer = DataWriter,
            coins=["TEST","HOW"],
            default_start_date=datetime.date(2021,6,21)
        )