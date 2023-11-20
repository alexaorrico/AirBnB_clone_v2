#!/usr/bin/python3
"""create a new view for City objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_state_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    cities = []
    for city in storage.all(City).values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def single_cities(city_id):
    """Retrives info for a single city"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city based on id"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Makes a city in a state"""
    obj = request.get_json()
    state_obj = storage.get(State, state_id)
    if not obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in obj:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if state_obj is None:
        abort(404)
    obj["state_id"] = state_id
    created_city = City(**obj)
    created_city.save()
    return make_response(jsonify(created_city.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a city"""
    city_obj = storage.get(City, city_id)
    obj = request.get_json()
    if city_obj is None:
        abort(404)
    if not obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in obj.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return make_response(jsonify(city_obj.to_dict()), 200)
