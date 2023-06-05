from storage_json import StorageJson
from OOP_MovieApp.movie_app import MovieApp


def main():
    """It contains the main function of the program."""
    # Create a StorageJson object
    storage = StorageJson("movies.csv")

    # Create a MovieApp object with the StorageJson object
    movie_app = MovieApp(storage)
    # Run the app
    movie_app.run()


if __name__ == "__main__":
    main()
