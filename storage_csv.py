import csv
from typing import Dict, Any
from OOP_MovieApp.istorage import IStorage
from OOP_MovieApp.movie_app import MovieApp
import requests
import json
import imdb


class StorageCsv(IStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.country_dict = {}

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        The function loads the information from the CSV file and returns the data.
        """
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            return reader

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
        Loads the information, add the movie, and saves it.

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
        except KeyError:
            print("Sorry, movie title does not exist!")
        except Exception as e:
            print(f"Error, API is not accessible. Possible reasons: {e}")

        with open(self.file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=movies.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the movies' database.
        Loads the information, deletes the movie,
        and saves it. The function doesn't need to validate the input.

        Args:
            title(str): movie title to delete
        """
        movies = self.list_movies()
        if title in movies:
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=movies[title].keys())
                writer.writeheader()
                del movies[title]
                for movie in movies.values():
                    writer.writerow(movie)

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
        if title in movies:
            movies[title]['notes'] = notes
            fieldnames = ['title', 'year', 'rating', 'poster', 'notes']
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for movie in movies.values():
                    writer.writerow(movie)


storage = StorageCsv('movies.csv')
movie_app = MovieApp(storage)
movie_app.run()
