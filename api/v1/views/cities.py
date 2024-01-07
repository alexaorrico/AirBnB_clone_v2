#!/usr/bin/python3
""" City views modules """

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities(state_id):
    """Retrieves the list of all City objects based on the state_id"""
    state = storage.get(State, state_id)

    if state:
        cities = state.cities
        cities_list = []
        for city in cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city based on it's ID"""
    city = storage.get(City, city_id)

    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city based on it's ID"""
    city = storage.get(City, city_id)

    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city(state_id):
    """Adds a city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    new_city = City(**data)
    new_city.state_id = state.id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_list = ["id", "state_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_list:
            setattr(city, key, value)
        else:
            pass

    storage.save()
    return jsonify(city.to_dict()), 200
