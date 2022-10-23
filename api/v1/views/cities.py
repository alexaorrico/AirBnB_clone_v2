#!/usr/bin/python3

"""Module to handle city request Blueprint"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """return json array of all cities of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    return jsonify([val.to_dict() for val in cities])


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a new city"""
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if storage.get(State, state_id) is None:
        abort(404)
    body["state_id"] = state_id
    new_city = City(**body)
    new_city.save()
    if storage.get(City, new_city.id) is not None:
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_city(city_id):
    """Method to get a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a single city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>', methods=['PUT'])
def update_city(city_id):
    """update properties of a single city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    _exceptions = ["id", "created_at", "updated_at", "state_id"]
    for k, v in body.items():
        if k not in _exceptions:
            setattr(city, k, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
