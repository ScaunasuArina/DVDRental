import psycopg2 as pg
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
        print(f"query: {query}")

        return query

    def get_all_films(self):
        """
        Get information about all the available films
        :return: a list of tuples containing all the films
        """
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except:
            print("Unable to connect to database!")

        with conn.cursor() as cursor:
            cursor.execute("SELECT title, description, release_year, length, rating FROM film")
            all_rows = cursor.fetchall()

        conn.close()
        print(all_rows)
        return all_rows

    def get_film(self, film_name):
        """
        Get information about all the available films
        :return: a list of tuples containing all the films
        """
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except:
            print("Unable to connect to database!")

        query = "SELECT * FROM film \
                WHERE title = '%s'" %film_name

        with conn.cursor() as cursor:
            cursor.execute(query)
            film_row = cursor.fetchall()

        conn.close()
        return film_row

    def get_oldest_movie(self):
        """
        Get the oldest movie available in the database
        :return:
        """

        try:
            conn = pg.connect(database=db, user=user, password=password)
        except:
            print("Unable to connect to database!")

        with conn.cursor() as cursor:
            cursor.execute("SELECT title, release_year FROM film ORDER BY release_year ASC")
            oldest_movie = cursor.fetchone()
        conn.close()
        return oldest_movie

    def get_actors_from_film(self, film_name):
        """
        Get the name of all actors playing in a movie
        :param film_name:
        :return:
        """
        actors = []
        try:
            conn = pg.connect(database=db, user=user, password=password)
        except:
            print("Unable to connect to database!")

        query = "SELECT first_name, last_name FROM actor \
                INNER JOIN film_actor \
                ON actor.actor_id=film_actor.actor_id \
                INNER JOIN film \
                ON film_actor.film_id=film.film_id \
                WHERE title='%s';" % film_name

        with conn.cursor() as cursor:
            cursor.execute(query)
            all_rows = cursor.fetchall()
        conn.close()

        # format actor's name
        for actor in all_rows:
            full_name = actor[0] + ' ' + actor[1]
            actors.append(full_name)
        return actors

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
        except:
            print("Unable to connect to database!")

        # check given params:
        self.check_insert_film_params(kwargs)
        # create the query
        query = self.create_insert_film_query(kwargs)

        with conn.cursor() as cursor:
            cursor.execute(query)



film = Film()

# all_actors = film.get_actors_from_film('Zhivago Core')
# for actor in all_actors:
#     print(actor)

# oldest_movie = film.get_all_films()
# print(oldest_movie)


# film.add_new_movie()

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
# film.add_new_movie(**film_info)

# dt = datetime.datetime.now()
# film_info={
#     'title': 'The Hunger Games',
#     'language_id': 1,
#     'length': 120,
#     'last_update': dt
# }
# film.add_new_movie(**film_info)

# print(film.get_film(film_info['title']))