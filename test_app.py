import sys
import pytest
from unittest.mock import patch
from main import main
from storage_json import StorageJson
from storage_csv import StorageCsv


def test_json_storage():
    """ Test instantiation of StorageJson. """
    storage = StorageJson("test.json")
    assert isinstance(storage, StorageJson)


def test_csv_storage():
    """  Test instantiation of StorageCsv. """
    storage = StorageCsv("test.csv")
    assert isinstance(storage, StorageCsv)


def test_main_invalid_argument(capsys):
    """ Run the main function with invalid arguments. """
    sys.argv = ['main.py']
    main()
    captured = capsys.readouterr()
    assert captured.out == "Usage: python3 main.py <storage_file>\n"


def test_main_unsupported_format():
    """ Run the main function with an unsupported storage file format. """
    with patch.object(sys, 'argv', ['main.py', 'storage.txt']):
        with pytest.raises(TypeError, match="Unsupported storage file format."):
            main()


pytest.main()
