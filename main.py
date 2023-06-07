import sys
from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp


def main():
    """It contains the main function of the program."""
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <storage_file>")
        return
    storage_file = sys.argv[1]

    if storage_file.endswith(".json"):
        storage = StorageJson(storage_file)
    elif storage_file.endswith(".csv"):
        storage = StorageCsv(storage_file)
    else:
        print("Unsupported storage file format.")
        return None

    # Create a MovieApp object with the StorageJson object
    movie_app = MovieApp(storage)
    # Run the app
    movie_app.run()


if __name__ == "__main__":
    main()
