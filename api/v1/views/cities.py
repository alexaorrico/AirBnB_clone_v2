#!/usr/bin/python3
"""
documenting module just to pass
checkers
"""

from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.state import State, City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def citiesByState(state_id):
    """cities by states"""

    if not storage.get(State, state_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    state = storage.get(State, state_id)
    cities = [x.to_dict() for x in state.cities]
    return jsonify(cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def citiesByIds(city_id):
    """cities by ids"""
    if not storage.get(City, city_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    city = storage.get(City, city_id)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def citiesDelete(city_id):
    """cities to delete by ids"""
    if not storage.get(City, city_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    city = storage.get(City, city_id)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def citiesPost(state_id):
    """posting new city"""

    data_obj = request.get_json()
    if not storage.get(State, state_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    if not data_obj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data_obj:
        return make_response(jsonify({"error": "Missing name"}), 400)
    data_obj["state_id"] = state_id
    new_city = City()
    for key, value in data_obj.items():
        setattr(new_city, key, value)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def citiesUpdate(city_id):
    """update cities"""
    if not storage.get(City, city_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    upt_data = request.get_json()
    if not upt_data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(City, city_id)
    for key, value in upt_data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(obj, key, value)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)