import psycopg2 as pg
from response_util import format_response
from Database.database_error_messages import database_error_msg
import datetime

db = 'dvdrental'
user = 'postgres'
password = 'admin'


class Film:
    def check_insert_film_params(self, kwargs):
        if len(kwargs) == 0:
            raise AttributeError('No arguments were given!')
        # # check required attributes 'title' and 'language_id'
        # if 'title' not in kwargs or 'language_id' not in kwargs:
        #     raise AttributeError('title and language_id are required attributes!')
        
    def create_insert_film_query(self, kwargs):
        col_text = ""
        val_text = ""
        columns = kwargs.keys()
        values = kwargs.values()

        for col in columns:
            col_text = col_text + str(col) + ","
        # remove last added comma
        col_text = col_text[:-1]

        for val in values:
            if isinstance(val, int):
                val_text = val_text + str(val) + ","
            else:
                val_text = val_text + "\'" + str(val) + "\'" + ","

        # remove last added comma
        val_text = val_text[:-1]

        query = "INSERT INTO film("+ col_text + ") " + "VALUES(" + val_text + ");"
        return query

    def get_all_films(self):
        """
        Get information about all the available films
        :return: a list of tuples containing all the films
        """
        col_text = ""
        all_films = []

        # form the query
        columns = ['title', 'description', 'release_year', 'name', 'length', 'replacement_cost', 'rating']
        for col in columns:
            col_text = col_text + str(col) + ", "
        # remove last added comma
        col_text = col_text[:-2]

        query = "SELECT " + col_text + " FROM film \
                INNER JOIN language \
                ON film.language_id = language.language_id"

        # connect to database and send query
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except pg.OperationalError:
            print(database_error_msg._NO_DATABASE_CONNECTION)
            return [database_error_msg._NO_DATABASE_CONNECTION]
        with conn.cursor() as cursor:
            cursor.execute(query)
            all_rows = cursor.fetchall()
        conn.close()

        # format response for each film
        for film in all_rows:
            response = format_response(columns, film)
            # convert replacement_cost from SQL Decimal to float
            response['replacement_cost'] = float(response['replacement_cost'])
            all_films.append(response)

        return all_films

    def get_film(self, film_name):
        """
        Get information about all the available films
        :return: A list of dictionaries containing all the films and their info.
        """
        col_text = ""
        film = []
        # form the query
        columns = ['title', 'description', 'release_year', 'name', 'length', 'replacement_cost', 'rating']
        for col in columns:
            col_text = col_text + str(col) + ", "
        # remove last added comma
        col_text = col_text[:-2]

        query = "SELECT " + col_text + " FROM film \
                        INNER JOIN language \
                        ON film.language_id = language.language_id \
                        WHERE title = '%s' " % film_name

        # connect to database and send query
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except pg.OperationalError:
            print(database_error_msg._NO_DATABASE_CONNECTION)
            return [database_error_msg._NO_DATABASE_CONNECTION]
        with conn.cursor() as cursor:
            cursor.execute(query)
            film_row = cursor.fetchall()
        conn.close()

        # format response
        for i in range(len(film_row)):
            # in case of multiple rows for the same movie, we will find multiple entries
            response = format_response(columns, film_row[i])
            # convert replacement_cost from SQL Decimal to float
            response['replacement_cost'] = float(response['replacement_cost'])
            film.append(response)

        return film

    def get_actors_from_film(self, film_name):
        """
        Get the name of all actors playing in a movie
        :param film_name: Title of the movie
        :return: A list with all actors playing in the movie.
        """
        actors = []
        query = "SELECT first_name, last_name FROM actor \
                INNER JOIN film_actor \
                ON actor.actor_id=film_actor.actor_id \
                INNER JOIN film \
                ON film_actor.film_id=film.film_id \
                WHERE title='%s';" % film_name

        # connect to database and send query
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except pg.OperationalError:
            print(database_error_msg._NO_DATABASE_CONNECTION)
            return [database_error_msg._NO_DATABASE_CONNECTION]
        with conn.cursor() as cursor:
            cursor.execute(query)
            all_rows = cursor.fetchall()
        conn.close()

        # format name
        for actor in all_rows:
            full_name = actor[0] + ' ' + actor[1]
            actors.append(full_name)

        return actors

    def get_oldest_movie(self):
        """
        Get the oldest movie available in the database.
        :return: A dictionary containing all the info about the film.
        """
        col_text = ""
        # form the query
        columns = ['title', 'description', 'release_year', 'length', 'replacement_cost', 'rating']
        for col in columns:
            col_text = col_text + str(col) + ", "
        # remove last added comma
        col_text = col_text[:-2]

        query = "SELECT " + col_text + " FROM film ORDER BY release_year ASC"

        # connect to database and send query
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except pg.OperationalError:
            print(database_error_msg._NO_DATABASE_CONNECTION)
            return database_error_msg._NO_DATABASE_CONNECTION
        with conn.cursor() as cursor:
            cursor.execute(query)
            oldest_movie = cursor.fetchone()
        conn.close()

        # format response
        response = format_response(columns, oldest_movie)
        # convert replacement_cost from SQL Decimal to float
        response['replacement_cost'] = float(response['replacement_cost'])

        return response

    def get_longest_movie(self):
        """
        Get the film with the longest length.
        :return: A dictionary containing all the info about the film.
        """
        col_text = ""
        # form the query
        columns = ['title', 'description', 'release_year', 'length', 'replacement_cost', 'rating']
        for col in columns:
            col_text = col_text + str(col) + ", "
        # remove last added comma
        col_text = col_text[:-2]

        query = "SELECT " + col_text + " FROM film ORDER BY length DESC"

        # connect to database and send query
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except pg.OperationalError:
            print(database_error_msg._NO_DATABASE_CONNECTION)
            return database_error_msg._NO_DATABASE_CONNECTION
        with conn.cursor() as cursor:
            cursor.execute(query)
            oldest_movie = cursor.fetchone()
        conn.close()

        # format response
        response = format_response(columns, oldest_movie)
        # convert replacement_cost from SQL Decimal to float
        response['replacement_cost'] = float(response['replacement_cost'])

        return response

    def add_new_movie(self, **kwargs):
        '''
        Add a new movie to database.
        :param title: Title of the film. Required information
        :param description: Description of the movie.
        :param release_year: Realease year of the film
        :param language_id: Language of the movie. Required information
        :param rental_duration: Durantion of the rental
        :param rental_rate: Rental cost
        :param length: Duration of the movie
        :param replacement_cost: Cost of replacing the movie in case of lost/deterioration
        :param rating: Rating of the movie
        :param last_update: Date of the last update
        :param special_features: Extra features of the movie
        :return:
        '''

        print(f"kwargs:{kwargs}")
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except pg.OperationalError:
            print(database_error_msg._NO_DATABASE_CONNECTION)
            return database_error_msg._NO_DATABASE_CONNECTION

        # check given params:
        self.check_insert_film_params(kwargs)
        # create the query
        query = self.create_insert_film_query(kwargs)

        with conn.cursor() as cursor:
            cursor.execute(query)
        return 1


film = Film()
getFilm = film.get_film
getAllFilms = film.get_all_films
getActorsFromFilm = film.get_actors_from_film
getOldestMovie = film.get_oldest_movie
getLongestMovie = film.get_longest_movie


# film_info={
#     'title': 'The Hunger Games'
# }
# film.add_new_movie(**film_info)

# film_info={
#     'title': 'The Hunger Games',
#     'language_id':1
# }
# film.add_new_movie(**film_info)

# film_info={
#     'title': 'The Hunger Games',
#     'language_id': 1,
#     'length': 120
# }
# # film.add_new_movie(**film_info)
# print(film.create_insert_film_query(film_info))

# dt = datetime.datetime.now()
# film_info={
#     'title': 'The Hunger Games',
#     'language_id': 1,
#     'length': 120,
#     'last_update': dt
# }
# film.add_new_movie(**film_info)

# print(film.get_film(film_info['title']))

# Raises psycopg2.OperationalError
# conn = pg.connect(database=db, user=user, password=password)

