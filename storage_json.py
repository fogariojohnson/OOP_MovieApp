
from OOP_MovieApp.istorage import IStorage
import json
import requests
import imdb


class StorageJson(IStorage):
    """A class that provides storage functionality for movies using JSON format."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.country_dict = {}

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.
        """
        with open(self.file_path, "r") as file_obj:
            file = json.loads(file_obj.read())
        return file

    def get_country_code(self):
        """ Creates country code

        Returns:
            country_dict(dict): A dictionary of countries and its code
        """
        api_key_holiday = "a47a88cb-3005-44d5-99d8-81710c7975cb"
        country_list = requests.get(f"https://holidayapi.com/v1/countries?pretty&key={api_key_holiday}")
        res = country_list.json()
        countries = res["countries"]
        dictionary = {}
        for country in countries:
            country_entry = country['name']
            code_entry = country['code']
            dictionary[country_entry] = code_entry
        self.country_dict = dictionary
        return self.country_dict

    @staticmethod
    def genre_maker(genre):
        """ Creates a genre image of the movie

        Args:
            genre(str): Emoticon to display

        Returns:
            character(str): A link to the character image
        """
        api_key = "RRhRnIM0DDVn6BbmwULBzQ==n9DVxWtNtkN2nwH5"
        api_url = 'https://api.api-ninjas.com/v1/emoji?name={}'.format(genre)
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        list_options = response.json()
        for char in list_options:
            character = char["image"]
        return character

    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movies' database.
        Loads the information from the JSON file, add the movie,
        and saves it.

        Args:
            title(str): title of the movie
            year(int): year the movie was released
            rating(float): rating of the movie
            poster(url): link to the poster of the movie(image)

        Raises:
            KeyError: If key is not found in the database
            Exception: Covers all the other error that might occur and explains user the reason.
        """
        # API for omdb
        api_key = "e2e17332"
        url_omd = f"http://www.omdbapi.com/?apikey={api_key}&t="

        # To locate the URL of the added movie
        ia = imdb.IMDb()
        add_movie = ia.search_movie(title)
        movie = add_movie[0]
        ia.update(movie)
        imdb_url = ia.get_imdbURL(movie)

        # To create the flag image of the added movie
        add_url = url_omd + title
        movie = requests.get(add_url)
        res = movie.json()
        country = res["Country"]
        if "," in country:
            country = country.split(",")[0]
        country_code = self.get_country_code()
        country_origin = country_code[country]

        # To create the genre image of the added movie
        genre_source = res["Genre"]
        first_genre = genre_source.split(",")[0]
        dict_of_genre_emoticons = {
            "Horror": "vampire",
            "Action": "bomb",
            "Western": "cowboy hat face",
            "Adventure": "person climbing",
            "Animation": "mage",
            "Comedy": "clown face",
            "Crime": "kitchen knife",
            "Drama": "loudly crying face",
            "Fantasy": "fairy",
            "Mystery": "detective",
            "Romance": "kiss",
            "Science Fiction": "alien",
            "Thriller": "ogre",
            "War": "crossed swords"
        }
        for key in dict_of_genre_emoticons.keys():
            if key == first_genre:
                genre = dict_of_genre_emoticons[key]
                movie_genre = self.genre_maker(genre)

        try:
            with open(self.file_path, "r") as file_obj:
                movies = json.load(file_obj)
            new_movie = {
                title: {
                    "rating": rating,
                    "year": int(year),
                    "poster url": poster,
                    "imdb_link": imdb_url,
                    "flag": f"https://flagsapi.com/{country_origin}/shiny/64.png",
                    "genre": movie_genre
                }
            }
            movies.update(new_movie)

            with open(self.file_path, "w") as new_info:
                json.dump(movies, new_info, indent=4, separators=(',', ':'))
        except KeyError:
            print("Sorry, movie title does not exist!")
        except Exception as e:
            print(f"Error, API is not accessible. Possible reasons: {e}")

    def delete_movie(self, title):
        """
        Deletes a movie from the movies' database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.

        Args:
            title(str): movie title to delete
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            with open(self.file_path, "w") as new_info:
                json.dump(movies, new_info, indent=4, separators=(',', ':'))
        else:
            print(f"\033[31m Movie {title} doesn't exist.\033[0m")

    def update_movie(self, title, notes):
        """
        Updates a movie from the movies' database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.

        Args:
            title(str): movie title to update
            notes(str): notes for the movie
        """
        movies = self.list_movies()
        movies[title]["notes"] = notes

        with open(self.file_path, "w") as new_info:
            json.dump(movies, new_info, indent=4, separators=(',', ':'))


storage = StorageJson('movies.json')
# print(storage.list_movies())
# storage.add_movie(title="Titanic", year=1997, rating=7.9, poster="https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg")
# storage.delete_movie("Titanic")
# storage.update_movie("Titanic", "A story of Jack and Rose")
