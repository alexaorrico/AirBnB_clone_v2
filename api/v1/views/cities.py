#!/usr/bin/python3
""" Handle RESTful API request for states"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ GET ALL CITIES IN A SPECIFIC STATE"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_dict = []
    for city in cities:
        cities_dict.append(city.to_dict())

    return jsonify(cities_dict)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ Retrieves a specific City """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete a city"""
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city """

    if not request.get_json():
        abort(400, description="Not a JSON")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    data['state_id'] = state_id

    if 'name' in data:
        new_city = City(**data)
        new_city.save()
    else:
        abort(400, description="Missing name")

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """update a City """

    if not request.get_json():
        abort(400, description="Not a JSON")

    obj = storage.get(City, city_id)

    if not obj:
        abort(404)

    data = request.get_json()

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(obj, key, value)
    obj.save()

    return make_response(jsonify(obj.to_dict()), 200)
