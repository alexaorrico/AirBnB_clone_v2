#!/usr/bin/python3
"""Handles the states view
"""

# from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Gets the list containing all the cities
    """
    state = storage.get("State", state_id)
    if state is None:
        return abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """Gets a city by its ID
    """
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city
    """
    city = storage.get("City", city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a state
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in got_json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_city = City(**got_json)
    storage.new(new_city)
    new_city.state_id = state_id
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a city
    """
    got_json = request.get_json()
    if not got_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    city = storage.get("City", city_id)
    if city:
        for key, val in got_json.items():
            setattr(city, key, val)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    else:
        abort(404)
