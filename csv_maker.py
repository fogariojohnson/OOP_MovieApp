import csv


def default_movies(file_name):
    """ Creates the information of the default movies in CSV format.

    Args:
         file_name(str): File name in csv format

    Returns:
        movies(tabular): Table of movies in csv format
    """

    movies = [
        ["title", "rating", "year", "poster url", "imdb_link", "flag", "genre"],
        ["The Shawshank Redemption", 9.5, 1994, "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_SX300.jpg", "https://www.imdb.com/title/tt0111161/?ref_=nv_sr_srsg_0_tt_7_nm_1_q_The%2520Shawsha", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F62D.png"],
        ["Pulp Fiction", 9.6, 1994, "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", "https://www.imdb.com/title/tt0110912/?ref_=nv_sr_srsg_0_tt_7_nm_1_q_Pulp", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F52A.png"],
        ["The Room", 3.6, 2003, "https://m.media-amazon.com/images/M/MV5BN2IwYzc4MjEtMzJlMS00MDJlLTkzNDAtN2E4NGNkZjg0MDgxXkEyXkFqcGdeQXVyMjQwMDg0Ng@@._V1_SX300.jpg", "https://www.imdb.com/title/tt0368226/?ref_=nv_sr_srsg_1_tt_8_nm_0_q_The%2520Room", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F52A.png"],
        ["The Godfather", 9.2, 1972, "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", "https://www.imdb.com/title/tt0068646/?ref_=nv_sr_srsg_1_tt_7_nm_0_q_The%2520God", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F52A.png"],
        ["The Godfather: Part II", 9.0, 1974, "https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", "https://www.imdb.com/title/tt0071562/?ref_=nv_sr_srsg_0_tt_5_nm_3_q_The%2520Godfather%253A%2520Pa", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F52A.png"],
        ["The Dark Knight", 9.0, 2008, "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg", "https://www.imdb.com/title/tt0468569/?ref_=nv_sr_srsg_0_tt_8_nm_0_q_The%2520Dark", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F4A3.png"],
        ["12 Angry Men", 8.9, 1957, "https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg", "https://www.imdb.com/title/tt0050083/?ref_=nv_sr_srsg_0_tt_8_nm_0_q_12%2520Angry", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F52A.png"],
        ["Everything Everywhere All At Once", 8.9, 2022, "https://m.media-amazon.com/images/M/MV5BYTdiOTIyZTQtNmQ1OS00NjZlLWIyMTgtYzk5Y2M3ZDVmMDk1XkEyXkFqcGdeQXVyMTAzMDg4NzU0._V1_SX300.jpg", "https://www.imdb.com/title/tt6710474/?ref_=nv_sr_srsg_1_tt_7_nm_0_q_Everythi", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F4A3.png"],
        ["Forrest Gump", 8.8, 1994, "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg", "https://www.imdb.com/title/tt0109830/?ref_=nv_sr_srsg_0_tt_1_nm_7_q_Forrest", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F62D.png"],
        ["Star Wars: Episode V", 8.7, 1980, "https://m.media-amazon.com/images/M/MV5BYmU1NDRjNDgtMzhiMi00NjZmLTg5NGItZDNiZjU5NTU4OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", "https://www.imdb.com/title/tt0080684/?ref_=nv_sr_srsg_4_tt_7_nm_0_q_Star%2520Wars%253A%2520Episode%2520V", "https://flagsapi.com/US/shiny/64.png", "https://api-ninjas-data.s3.us-west-2.amazonaws.com/emojis/U%2B1F4A3.png"]
    ]

    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(movies)
    return writer
