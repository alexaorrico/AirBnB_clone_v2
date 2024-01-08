#!/usr/bin/python3
"""
handles all default RESTFul API actions for City objects
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get("State", state_id)
    if state:
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                  strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                  strict_slashes=False)
def create_city(state_id):
    """ Creates a City """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
