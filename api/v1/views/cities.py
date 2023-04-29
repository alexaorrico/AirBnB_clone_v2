#!/usr/bin/python3
"""
This is a new view for `City` objects that handles all default RESTful ops
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from . import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def read_create_city(state_id):
    """Handle `GET` and `POST` operations on `cities`"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    city_data = request.get_json(silent=True)
    if city_data is None:
        abort(400, "Not a JSON")
    if 'name' not in city_data:
        abort(400, "Missing name")

    new_city = City(state_id=state_id, name=city_data['name'])
    new_city.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT'])
def read_update_city(city_id):
    """Handles `GET` and `PUT` operations for cities"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    city_data = request.get_json(silent=True)
    if city_data is None:
        abort(400, "Not a JSON")

    city.name = city_data.get('name', city.name)
    city.state_id = city_data.get('state_id', city.state_id)
    city.save()

    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes the city with `city_id`"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response({}, 200)
