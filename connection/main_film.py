from user_credentials import users
from flask import Flask, json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from database.Film import getFilm, getAllFilms, getActorsFromFilm, getOldestMovie, getLongestMovie
from database.Film import addNewMovie, removeMovie
from database.database_error_messages import database_error_msg

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


@app.route('/films', methods=['GET'])
@auth.login_required
def get_all_films():
    films = getAllFilms()
    if database_error_msg._NO_DATABASE_CONNECTION in films:
        response = app.response_class(
            response=database_error_msg._NO_DATABASE_CONNECTION,
            status=500,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(films),
            status=200,
            mimetype='application/json'
        )
    return response


# this function is not called because we use the same URL
# we can add query params in the above function - they are optional
# @app.route('/films', methods=['GET'])
# def get_one_film():
#     title = request.args.get('title')
#     film_info = get_film(title)
#     return film_info

# ex. API call: http://127.0.0.1:7777/films/Desert Poseidon
# get film by using path parameters
@app.route('/films/<film_name>', methods=['GET'])
@auth.login_required
def get_film(film_name):
    film_info = getFilm(film_name)
    if database_error_msg._NO_DATABASE_CONNECTION in film_info:
        response = app.response_class(
            response=database_error_msg._NO_DATABASE_CONNECTION,
            status=500,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(film_info),
            status=200,
            mimetype='application/json'
        )
    return response


# ex. API call: http://127.0.0.1:7777/films/Desert Poseidon/actors
# get actors playing in a movie with query parameters
@app.route('/films/<film_name>/actors', methods=['GET'])
@auth.login_required
def get_actors_from_film(film_name):
    actors = getActorsFromFilm(film_name)
    if database_error_msg._NO_DATABASE_CONNECTION in actors:
        response = app.response_class(
            response=database_error_msg._NO_DATABASE_CONNECTION,
            status=500,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(actors),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/films/oldest', methods=['GET'])
@auth.login_required
def get_oldest_film():
    oldest_movie = getOldestMovie()
    if database_error_msg._NO_DATABASE_CONNECTION in oldest_movie:
        response = app.response_class(
            response=database_error_msg._NO_DATABASE_CONNECTION,
            status=500,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(oldest_movie),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route('/films/longest_film', methods=['GET'])
@auth.login_required
def get_longest_film():
    film_info = getLongestMovie()
    if database_error_msg._NO_DATABASE_CONNECTION in film_info:
        response = app.response_class(
            response=database_error_msg._NO_DATABASE_CONNECTION,
            status=500,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps(film_info),
            status=200,
            mimetype='application/json'
        )
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='7777')
