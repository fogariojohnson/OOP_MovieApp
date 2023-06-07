"""
===========================================================
                    Movie Application
              Object-Oriented Programming
              By Frelin C. Ogario Johnson
===========================================================
"""

import statistics
import sys
import requests
import random
import matplotlib.pyplot as plt


class MovieApp:
    """Movie app class represents a movie application"""
    def __init__(self, storage):
        """ Initializes a new instance of the MovieApp class. """
        self._storage = storage

    @staticmethod
    def exit_movie():
        """Exits the app and prints 'Bye'."""
        print("Bye!")
        sys.exit()

    def _command_list_movies(self):
        """ Displays the dictionary of movies. """
        movies = self._storage.list_movies()
        print(f"{len(movies)} movies in total")
        for key, value in movies.items():
            print(f"\033[34m{key}\n\033[0mRating: {value['rating']}\nYear: {value['year']}")

    def _command_add_movie(self):
        """ Adds a movie. """
        title = input("Enter new movie name: ")
        api_key = "e2e17332"
        url_omd = f"http://www.omdbapi.com/?apikey={api_key}&t="

        try:
            add_url = url_omd + title
            movie = requests.get(add_url)
            res = movie.json()
            rating_values = [float(rating['Value'][0][:3]) for rating in res['Ratings']]
            rating = float(rating_values[0])
            movie_title = res["Title"]
            year = int(res["Year"])
            poster = res["Poster"]
            self._storage.add_movie(movie_title, int(year), float(rating), poster)
            print(f"\033[34m Movie {title} successfully added. \033[0m")
        except KeyError:
            print("Sorry, movie title does not exist!")
        except Exception as e:
            print(f"Error, API is not accessible. Possible reasons: {e}")

    def _command_delete_movie(self):
        """ Deletes a movie """
        movies = self._storage.list_movies()
        movie_name = input("Enter movie name to delete: ")
        if movie_name in movies:
            self._storage.delete_movie(movie_name)
            print(f"The movie {movie_name} successfully deleted")
        else:
            print(f"\033[31m Movie {movie_name} doesn't exist."
                  f" Choose from the following movies \033[0m")
            self._command_list_movies()

    def _command_update_movie(self):
        """ Adds notes to the movie. """
        movies = self._storage.list_movies()
        movie_name = input("Enter movie name: ")
        if movie_name in movies:
            movie_note = input("Enter movie notes: ")
            self._storage.update_movie(movie_name, movie_note)
            print(f'The movie "{movie_name}" is successfully updated.')
        else:
            print(f"\033[31m Movie {movie_name} doesn't exist."
                  f" Choose from the following movies \033[0m")
            self._command_list_movies()

    def movie_stats(self):
        """
        Displays the statistics of the movies in the dictionary.
        It includes the average rating, median rating, the best movie, and worst movie.
        """
        movies = self._storage.list_movies()

        # Identifies the median rating of all the movies in the dictionary
        ratings = [value["rating"] for value in movies.values()]
        total_rating = sum(ratings)
        average_rating = total_rating / len(ratings)
        print(f"Average: {average_rating:.2f}")
        median_rating = statistics.median(ratings)
        print(f"Median rating: {median_rating:.2f}")

        # Identifies the best and worst rating of all the movies in the dictionary
        key_ratings = [(key, value["rating"]) for key, value in movies.items()]
        max_key, max_rating = max(key_ratings, key=lambda x: x[1])
        min_key, min_rating = min(key_ratings, key=lambda x: x[1])
        print(f"Best movie: {max_key} ({max_rating:.2f})")
        print(f"Best movie: {min_key} ({min_rating:.2f})")

    def random_movie(self):
        """ Randomly choose a movie. """
        movies = self._storage.list_movies()
        key, value = random.choice(list(movies.items()))
        print(f"Your movie tonight: {key}, it's rated {value['rating']}")

    def search_movie(self):
        """ Search a movie title[key] and its possible matching string. """
        movies = self._storage.list_movies()
        movie_name = input("Enter a search term: ")
        lowercase_movie_name = movie_name.lower()
        found_movies = []
        for movie, rating in movies.items():
            lowercase_movies = movie.lower()
            if lowercase_movie_name in lowercase_movies:
                found_movies.append((movie, rating['rating']))
        if found_movies:
            found_movies.sort(key=lambda x: x[1], reverse=True)
            for movie, rating in found_movies:
                print(f"{movie}, {rating}")
        else:
            print(f"The search term {movie_name} is not found")
            # self.search_movie_distance(movie_name)

    def sorted_movie(self):
        """ Sorts the movie title[key] based on its rating(value) in descending order. """
        movies = self._storage.list_movies()
        sorted_movies = dict(sorted(movies.items(),
                                    key=lambda x: x[1]['rating'], reverse=True))
        for key, value in sorted_movies.items():
            print(f"{key}: {value['rating']}")

    def movie_histogram(self):
        """ Allows user to save the histogram of ratings in different file type specified

        Returns:
            None
        """
        movies = self._storage.list_movies()
        rating_list = []
        for value in movies.values():
            rating_list.append(value['rating'])
        plt.hist(rating_list, bins=5)
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Rating")
        plt.ylabel("Count")
        plt.title("Movie Rating")
        filename = input("Choose a filename for your histogram: ")
        filetype = input("In which filetype do you want to save the histogram as? ")
        # Checking the supported format
        if filetype in "eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff":
            file_name = filename + "." + filetype
            plt.savefig(file_name)
            print(f'"{file_name}" is successfully created')
        else:
            print("Format is not supported. Please try a different file format")
            self.run()

    def _html_structure(self):
        """
        Creates the HTML structure

        Returns:
             output: HTML structure
        """
        movies = self._storage.list_movies()
        output = " "
        for title, stat in movies.items():
            if "poster url" not in stat or not stat["poster url"]:
                poster = None
            else:
                poster = stat["poster url"]
            if "flag" not in stat or not stat["flag"]:
                flag = None
            else:
                flag = stat["flag"]
            if "imdb_link" not in stat or not stat["imdb_link"]:
                imd_url = None
            else:
                imd_url = stat["imdb_link"]
            if "genre" not in stat or not stat["genre"]:
                genre = None
            else:
                genre = stat["genre"]
            if "notes" not in stat or not stat["notes"]:
                notes = None
            else:
                notes = stat["notes"]

            movie_title = title
            rating = stat["rating"]
            year = stat["year"]

            output += '\t<li>\n'
            output += '\t\t<div class="movie">\n'
            output += f'<a href ="{imd_url}"\n>'
            output += '\t\t\t<img class="movie-poster"\n'
            if notes is None:
                output += f'\t\t\t\tsrc="{poster}"\n\t\t\t\ttitle="" alt ="{movie_title}"/></a>\n'
            else:
                output += f'\t\t\t\tsrc="{poster}"\n\t\t\t\ttitle="{notes}" alt ="{movie_title}"/></a>\n'
            output += f'\t\t\t\t<img src={flag} class="flag" alt="flag origin">\n'
            output += f'\t\t\t<div class="movie-title">{movie_title}</div>\n'
            output += f'\t\t\t<div class="movie-rating">Rating: {rating}</div>\n'
            output += f'\t\t\t<img src={genre} alt="emoticon">\n'
            output += f'\t\t\t<div class="movie-year">{year}</div>\n'
            output += '\t\t</div>\n\t</li>\n'
        return output

    def _generate_website(self):
        """
        Loads HTML file template and creates a new HTML file.

        Returns:
            data(dict): the movies' dictionary
        """
        # Reads the existing html template
        with open("index_template.html", "r") as file_obj:
            data = file_obj.read()

        with open("../movie_app.html", "w") as new_file:
            new_data = self._html_structure()
            new_content = data.replace("__TEMPLATE_TITLE__", "My Collection of Movies")
            new_content = new_content.replace("__TEMPLATE_MOVIE_GRID__", new_data)
            new_file.write(new_content)
            print("Website was generated successfully")

    def end_prompt(self):
        """Prompts user to press Enter key every end of the method or function"""
        enter = input("\033[33m" + "Please enter to continue " + "\033[0m")
        if enter == "":
            self.run()
        else:
            print("\033[31m" + "Error! Please press Enter key to continue" + "\033[0m")
            self.run()

    def run(self):
        """
        Displays a menu and allows the user to choose from a list of options.
        """
        try:
            print("\033[36m Menu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n"
                  "4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n"
                  "8. Movies sorted by rating\n9. Creating Rating Histogram\n"
                  "10. Generate website\033[0m")
            # Define the functions for each choice
            functions = {
                0: self.exit_movie,
                1: self._command_list_movies,
                2: self._command_add_movie,
                3: self._command_delete_movie,
                4: self._command_update_movie,
                5: self.movie_stats,
                6: self.random_movie,
                7: self.search_movie,
                8: self.sorted_movie,
                9: self.movie_histogram,
                10: self._generate_website
            }

            # Get the user's choice
            choice = int(input("Enter your choice: "))

            if choice in functions:
                functions[choice]()
                self.end_prompt()
            else:
                print("\033[31m" + "Error! Please choose from numbers 0 to 10." + "\033[0m")
                self.run()
        except ValueError:
            print("\033[31m" + "Error! Please choose from numbers 0 to 10." + "\033[0m")
            self.run()


"""Use to test the code."""
# if __name__ == "__main__":
#     storage_file = StorageJson('movies.json')
#     movie_app = MovieApp(storage_file)
#     movie_app.run()
