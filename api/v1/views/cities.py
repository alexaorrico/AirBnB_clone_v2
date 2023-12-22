#!/usr/bin/python3
"""api/v1/views/cities.py"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_get_all(state_id):
    """all state instances of city objects"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_get(city_id):
    """gets a city instance"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_delete(city_id):
    """deletes a city instance"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_create(state_id):
    """creates a city instance"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    elif "name" not in request.get_json():
        abort(400, description="Missing name")
    city = City(state_id=state_id, **request.get_json())
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def cities_put(city_id):
    """updates a city instance"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
