import csv
from istorage import IStorage
import requests
import imdb
import csv_maker


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        self.country_dict = {}

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the CSV
        file and returns the data.
        """
        try:
            movies = {}
            with open("ashley.csv", 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row['title']
                    movies[title] = {
                        "rating": float(row['rating']),
                        "year": int(row['year']),
                        "poster url": (row['poster url']),
                        "imdb_link": (row['imdb_link']),
                        "flag": (row['flag']),
                        "genre": (row['genre']),
                    }
            return movies
        except FileNotFoundError:
            print(f"{self.file_path}not found. Please wait while I load default data.")
            reader = csv_maker.default_movies(self.file_path)
            for row in reader:
                title = row['title']
                movies[title] = {
                    "rating": float(row['rating']),
                    "year": int(row['year']),
                    "poster url": (row['poster url']),
                    "imdb_link": (row['imdb_link']),
                    "flag": (row['flag']),
                    "genre": (row['genre']),
                }
            return movies

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

        flag = f"https://flagsapi.com/{country_origin}/shiny/64.png"
        try:
            with open(self.file_path, 'a', newline='') as new_file:
                writer = csv.writer(new_file)
                writer.writerow([title, float(rating), int(year), poster, imdb_url, flag, movie_genre])

        except KeyError:
            print("Sorry, movie title does not exist!")
        except Exception as e:
            print(f"Error! Possible reasons: {e}")

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
            del movies[title]
            self.save_movies(movies)
            print(f"The movie '{title}' has been deleted.")
        else:
            print(f"The movie '{title}' does not exist.")

    def update_movie(self, title, notes):
        """
        Updates a movie from the movies' database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.

        Args:
            title(str): movie title to update
            notes(str): notes for the movie
        """
        """
                Updates a movie's notes in the database based on its title.

                The function loads the movie information from the CSV file,
                updates the notes of the specified movie entry, and saves the updated data back to the file.
                """
        movies = self.list_movies()
        if title in movies:
            movies[title]['notes'] = notes
            self.save_movies(movies)
            print(f"The notes for the movie '{title}' have been updated.")
        else:
            print(f"The movie '{title}' does not exist.")

    def save_movies(self, movies):
        """
        Saves the movie information to the CSV file.

        The function takes a dictionary of dictionaries representing the movie data,
        converts it to a list of dictionaries, and writes it to the CSV file.
        """
        fieldnames = ['title', 'rating', 'year', 'poster url', 'imdb_link', 'flag', 'genre']
        rows = [movies[title] for title in movies]

        with open(self.file_path, 'w', newline='') as new_file:
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


# storage = StorageCsv('movies.csv')
# movie_app = MovieApp(storage)
# movie_app.run()
