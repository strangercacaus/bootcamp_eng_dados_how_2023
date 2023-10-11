import sys
import pytest
import datetime

from unittest.mock import patch, mock_open

from M04_API.code.ingestors import DataIngestor
from M04_API.code.writers import DataWriter

@pytest.fixture
@patch("M04_API.code.ingestors.DataIngestor.__abstractmethods__", set())
def data_ingestor_fixture():
    return DataIngestor(
            writer = DataWriter,
            coins=["TEST","HOW"],
            default_start_date=datetime.date(2021,6,21)
        )

class TestDataIngestors:
    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert actual == expected

    def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        excpected = datetime.date(2021,6,21)
        assert actual == excpected
    
    @patch("builtins.open", new_callable = mock_open, read_data="2021-06-25")
    def test_load_checkpoint_with_checkpoint(self, mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        excpected = datetime.date(2021,6,25)
        assert actual == excpected
    
    @patch("M04_API.code.ingestors.DataIngestor._write_checkpoint",return_value = None)
    def test_update_checkpoint_checkpoint_updated(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.date(2019,1,1))
        actual = data_ingestor._checkpoint
        excpected = datetime.date(2019,1,1)
        assert actual == excpected

    @patch("M04_API.code.ingestors.DataIngestor._write_checkpoint",return_value = None)
    def test_update_checkpoint_checkpoint_written(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.date(2019,1,1))
        mock.assert_called_once()

    @patch("M04_API.code.ingestors.DataIngestor._checkpoint_filename",return_value='foobar.checkpoint')
    @patch("builtins.open", new_callable=mock_open, read_data='2021-06-25')
    def test_write_checkpoint(self, mock_open_file, mock_checkpoint_filename, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._write_checkpoint()
        mock_open_file.assert_called_with(mock_checkpoint_filename,'w')