import sys
import pytest
from unittest.mock import patch
from main import main
from movie_app import MovieApp


def test_main_json_storage():
    # Run the main function with a JSON storage file
    with patch.object(sys, 'argv', ['main.py', 'storage.json']):
        main()


def test_main_csv_storage():
    # Run the main function with a CSV storage file
    with patch.object(sys, 'argv', ['main.py', 'storage.csv']):
        main()


def test_main_invalid_argument():
    # Run the main function with invalid arguments
    with patch.object(sys, 'argv', ['main.py']):
        with pytest.raises(SystemExit):
            main()


def test_main_unsupported_format():
    # Run the main function with an unsupported storage file format
    with patch.object(sys, 'argv', ['main.py', 'storage.txt']):
        with pytest.raises(SystemExit):
            main()


pytest.main()
