#!/usr/bin/python3
"""This module is in charge of handling requests for state-type objects."""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def states_id_cities(state_id):
    """Get a specific City object through the HTTP GET request."""
    if storage.get(State, state_id) is None:
        abort(404)
    all_cities = []
    for city in storage.all(City).values():
        if city.state_id == state_id:
            all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_id_post(state_id):
    """Create a new City object through the HTTP POST request."""
    obj_state = storage.get(State, state_id)
    if obj_state:
        if request.get_json():
            if "name" in request.get_json():
                obj = City(**request.get_json(), state_id=state_id)
                storage.new(obj)
                storage.save()
                return obj.to_dict(), 201
            return jsonify({"error": "Missing name"}), 400
        return jsonify({"error": "Not a JSON"}), 400
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cities_id(city_id):
    """Get a specific City object through the HTTP GET request."""
    obj = storage.get(City, city_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def cities_id_delete(city_id):
    """Delete a specific City object through the HTTP DELETE request."""
    obj = storage.get(City, city_id)
    if obj is not None:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def city_id_put(city_id):
    """Update a specific City object through the HTTP PUT request."""
    obj = storage.get(City, city_id)
    if obj is not None:
        if request.get_json():
            fix_dict = request.get_json()
            attributes = ["id", "created_at", "updated_at"]
            for k, v in fix_dict.items():
                if k not in attributes:
                    setattr(obj, k, v)
            obj.save()
            return jsonify(obj.to_dict()), 200
        return jsonify({"error": "Not a JSON"}), 400
    abort(404)
