#!/usr/bin/python3

""" Handles all restful API actions for State"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.state import State
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """ Returns all cities from state id """

    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    all_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_individual_cities(city_id):
    """" Returns indivuidual cities by id """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes individual states by id """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    """ Delete the state """
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a new city by using the URL """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    my_dict = request.get_json()
    if my_dict is None:
        abort(400, 'Not a JSON')
    if my_dict.get("name") is None:
        abort(400, 'Missing name')

    my_dict["state_id"] = state_id
    new_city = City(**my_dict)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Updates a city by City ID """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    my_dict = request.get_json()

    if my_dict is None:
        abort(400, 'Not a JSON')

    city.name = my_dict.get("name")
    city.save()
    return jsonify(city.to_dict()), 200
