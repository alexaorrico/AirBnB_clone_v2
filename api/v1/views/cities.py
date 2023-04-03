#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities_list = []
    cities = storage.all("City").values()
    for city in cities:
        if city.state_id == state.id:
            cities_list.append(city.to_json())
    return jsonify(cities_list)


@app_views.route("/cities/<string:city_id>", methods=['GET'])
def city_get(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city = city.to_json()
    return jsonify(city)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def city_delete(city_id):
    """Deletes a City object"""
    dict = {}
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify(dict), 200


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """Creates a City"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing a name")
    city = City(**data)
    city.state_id = state_id
    city.save()
    city = city.to_json()
    return jsonify(city), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def city_update(city_id):
    """Updates a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        keys = ["id", "created_at", "updated_at"]
        if key not in keys:
            city.bm_update(key, value)
    city.save()
    city = city.to_json()
    return jsonify(city), 200
