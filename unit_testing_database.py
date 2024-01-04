from unittest import TestCase, mock
import psycopg2 as pg
from Database.Film import Film
import coverage

from Database.database_error_messages import database_error_msg

film = Film()
class Test(TestCase):
    def test_get_all_films(self):
        expected_output = 1001
        assert len(film.get_all_films()) == expected_output

    def test_get_film(self):
        film_name = 'Desert Poseidon'
        expected_output = [
            {'title': 'Desert Poseidon',
             'description': 'A Brilliant Documentary of a Butler And a Frisbee who must Build a Astronaut in New Orleans',
             'release_year': 2006,
             'name': 'English',
             'length': 64,
             'replacement_cost': 27.99,
             'rating': 'R'}
        ]
        assert film.get_film(film_name) == expected_output

    def test_get_actors_from_film(self):
        film_name = 'Desert Poseidon'
        expected_output = ['Goldie Brody', 'Henry Berry', 'Burt Posey', 'Liza Bergman', 'Renee Ball']
        assert film.get_actors_from_film(film_name) == expected_output

    def test_get_oldest_movie(self):
        expected_output = {
            'title': 'Chamber Italian',
            'description': 'A Fateful Reflection of a Moose And a Husband who must Overcome a Monkey in Nigeria',
            'release_year': 2006,
            'length': 117,
            'replacement_cost': 14.99,
            'rating': 'NC-17'
        }
        assert film.get_oldest_movie() == expected_output

    def test_get_longest_movie(self):
        expected_output = {
            'title': 'The Hunger Games',
            'description': 'description',
            'release_year': None,
            'length': None,
            'replacement_cost': 19.99,
            'rating': 'G'
        }
        assert film.get_longest_movie() == expected_output

    def test_check_insert_film_params(self):
        kwargs = []
        try:
            assert film.check_insert_film_params(kwargs) == AttributeError
        except AttributeError:
            pass

    def test_create_insert_film_query(self):
        film_info = {
            'title': 'The Hunger Games',
            'language_id': 1,
            'length': 120
        }
        expected_output = "INSERT INTO film(title,language_id,length) VALUES('The Hunger Games',1,120);"

        assert film.create_insert_film_query(film_info) == expected_output

