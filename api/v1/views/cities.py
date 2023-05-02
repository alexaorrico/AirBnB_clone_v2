#!/usr/bin/python3
"""

"""


from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    if 'name' not in data:
        abort(400, 'Missing name')

    city = City(**data)
    city.state_id = state_id
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    city.save()

    return make_response(jsonify(city.to_dict()), 200)
