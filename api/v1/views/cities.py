#!/usr/bin/python3
""" cities view module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities(state_id):
    """ Get cities under a given state """

    states = storage.all(State)

    if State.__name__ + '.' + state_id not in states.keys():
        abort(404)
    print('yesy')
    the_cities = storage.all(City)
    result = []
    for city in the_cities.keys():
        try:
            if the_cities[city].to_dict()['state_id'] == state_id:
                result.append(the_cities[city].to_dict())
        except KeyError:
            abort(404)
    return jsonify(result), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ Get data for a city """
    try:
        the_city = storage.all(City)[City.__name__ + '.' + city_id]
        return jsonify(the_city.to_dict()), 200
    except KeyError:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """ Delete a city """
    try:
        storage.all().pop(City.__name__ + '.' + city_id)
        storage.save()
        return jsonify({}), 200
    except KeyError:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Create a new city """
    states = storage.all(State)

    if State.__name__ + '.' + state_id not in states.keys():
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        abort(404, description='Not a JSON')

    if not data['name']:
        abort(404, description='Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()

    return jsonify(storage.get(City, city.id).to_dict())


@app_views.route('/cities/<city_id>', methods=['PUT'])
def edit_city(city_id):
    """ Edit a given city, with a given data """
    the_cities = storage.all(City)

    if City.__name__ + '.' + city_id not in the_cities.keys():
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        abort(404, description='Not a JSON')

    if not data['name']:
        abort(404, description='Missing name')

    city = City(**data)
    city.save()

    return jsonify(storage.get(City, city.id).to_dict())
