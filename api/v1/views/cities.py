#!/usr/bin/python3
"""
cities for API
"""
from flask import jsonify, abort, request
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of all City objects of a State
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    list_cities = []

    for city in state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cities_by_id(city_id):
    """Retrieves a City object
    """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_by_id_del(city_id):
    """Retrieves a City object
    """
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """ handles POST method
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    city = City(**data)
    city.state_id = state_id
    city.save()
    city = city.to_dict()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """PUT city
    """
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")
    else:

        for key, value in data.items():
            ignore_keys = ["id", "created_at", "updated_at"]
            if key in ignore_keys:
                pass
            else:
                setattr(city, key, value)
        storage.save()
        s = city.to_dict()
        return jsonify(s), 200
