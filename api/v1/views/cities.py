#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_get(state_id):
    """Retrieves the list of all City"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)

    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_post(state_id):
    """Creates a City"""
    transform_dict = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if transform_dict is None:
        abort(400, "Not a JSON")
    if 'name' not in transform_dict.keys():
        abort(400, "Missing name")
    else:
        transform_dict['state_id'] = state_id
        new_city = City(**transform_dict)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id_get(city_id):
    """Retrieves a City object and 404 if it's an error"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cities_id_delete(city_id):
    """ Function that deletes a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def cities_id_put(city_id):
    """Updates a City object"""
    ignore_list = ['id', 'created_at', 'updated_at']
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    for key, value in transform_dict.items():
        if key not in ignore_list:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
