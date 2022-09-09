#!/usr/bin/python3
"""
City
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """
    Retrieves the list of all City objects of the State
    """
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    cities_list = []
    for city in states.cities:
        cities_list.append(city.to_dict())
    return(jsonify(cities_list))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id(city_id):
    """
    Retrieves a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return (jsonify(city.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    if "name" not in request.get_json():
        no_name = {"error": "Missing name"}
        return (jsonify(no_name), 400)
    obj_dict = request.get_json()
    obj_dict['state_id'] = state.id
    city = City(**obj_dict)
    city.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        error = {"error": "Not a JSON"}
        return (jsonify(error), 400)
    obj_dict = request.get_json()
    city.name = obj_dict["name"]
    city.save()
    return (jsonify(city.to_dict()), 200)
