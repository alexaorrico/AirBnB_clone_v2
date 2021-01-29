#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_get(state_id=None):
    """retrieves the list of all City objects
    """
    state_info = storage.get("State", state_id)
    if state_info is None:
        abort(404)

    state_cities = state_info.cities
    cities_dict = [city.to_dict() for city in state_cities]
    return jsonify(cities_dict)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_get_error(city_id):
    """retrieves a City object
    """
    city = storage.get('City', city_id)
    if city:
        return city.to_dict()
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    """deletes a City object
    """
    del_city = storage.get('City', city_id)
    if del_city is None:
        abort(404)
    storage.delete(del_city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """creates a city
    """
    info = request.get_json(silent=True)
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    name = info.get('name')
    if name is None:
        return jsonify(abort(400, 'Missing name'))

    state_info = storage.get("State", state_id)
    if state_info is None:
        abort(404)

    new_city = City(**info)
    new_city.state_id = state_id
    new_city.name = name
    new_city.save()

    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """updates a state object
    """
    info = request.get_json()
    if info is None:
        return jsonify(abort(400, 'Not a JSON'))

    city_info = storage.get("City", city_id)
    if city_info is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at", "state_id"]
    for key, value in info.items():
        if key not in ignore_keys:
            setattr(city_info, key, value)

    city_info.save()
    return jsonify(city_info.to_dict())
