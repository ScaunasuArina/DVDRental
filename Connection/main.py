from flask import Flask, request, json
from Database.Film import Film

film = Film()

app = Flask(__name__)

@app.route('/films', methods=['GET'])
def get_all_films():
    films = film.get_all_films()
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

# ex. API call: http://127.0.0.1:5000/films/Desert Poseidon
# get film by using path parameters
@app.route('/films/<film_name>', methods=['GET'])
def get_film(film_name):
    film_info = film.get_film(film_name)
    response = app.response_class(
        response=json.dumps(film_info),
        status=200,
        mimetype='application/json'
    )
    return response

# ex. API call: http://127.0.0.1:5000/films/actors?title=Desert Poseidon
# get actors playing in a movie with query parameters
@app.route('/films/actors', methods=['GET'])
def get_actors_from_film():
    # get query parameters
    title = request.args.get('title')
    film_info = film.get_actors_from_film(title)
    response = app.response_class(
        response=json.dumps(film_info),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='7777')

