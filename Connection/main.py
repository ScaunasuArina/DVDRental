from flask import Flask, json
from Database.Film import getFilm, getAllFilms, getActorsFromFilm, getOldestMovie, getLongestMovie

app = Flask(__name__)

@app.route('/films', methods=['GET'])
def get_all_films():
    films = getAllFilms()
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
def get_film(film_name):
    film_info = getFilm(film_name)
    response = app.response_class(
        response=json.dumps(film_info),
        status=200,
        mimetype='application/json'
    )
    return response

# ex. API call: http://127.0.0.1:7777/films/Desert Poseidon/actors
# get actors playing in a movie with query parameters
@app.route('/films/<film_name>/actors', methods=['GET'])
def get_actors_from_film(film_name):
    actors = getActorsFromFilm(film_name)
    response = app.response_class(
        response=json.dumps(actors),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/films/oldest', methods=['GET'])
def get_oldest_film():
    oldest_movie = getOldestMovie()
    response = app.response_class(
        response=json.dumps(oldest_movie),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/films/longest_film', methods=['GET'])
def get_longest_film():
    film_info = getLongestMovie()
    response = app.response_class(
        response=json.dumps(film_info),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='7777')

