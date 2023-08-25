#!/usr/bin/python3
""""""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
    methods=["GET"]
    )
def get_list_of_state_cities(state_id):
    """ module to get cities in states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    city_list = []
    for city in cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route(
    "/cities/<city_id>",
    strict_slashes=False,
    methods=["GET"]
    )
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        "/states/<state_id>/cities",
        strict_slashes=False,
        methods=["POST"]
    )
def create_new_city(state_id):
    state = State.get(State, state_id)
    if state is None:
        abort(404)
    new_city_JSON = request.get_json(silent=True)
    # if the JSON is invalid
    if new_city_JSON is None:
        abort(400, "Not a JSON")
    if 'name' not in new_city_JSON:
        abort(400, "Missing name")
    new_city_JSON['state_id'] = state_id
    new_city = City(**new_city_JSON)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route(
    "/cities/<city_id>",
    strict_slashes=False,
    methods=["DELETE"]
    )
def delete_city(city_id):
    """
    Deletes city object with 'city_id' as its 'id'
    field/column value (let's call it 'target')
    from 'storage.all' dictionary, by calling storage.delete(<target>)

    Returns ({}, 200) if successful,
    404 if 'target' doesn't exist.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}, 200)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)