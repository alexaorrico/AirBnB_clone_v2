#!/usr/bin/python3
"""View for City objects that handles all default RestFul API"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """List cities per state"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    all_cities = storage.all("City").values()
    st_cities = [c.to_dict() for c in all_cities if c.state_id == state_id]
    return jsonify(st_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_id(city_id):
    """Deletes a City object by id"""
    city_id = storage.get('City', city_id)
    if city_id is None:
        abort(404)
    storage.delete(city_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    new_city_dict = request.get_json(silent=True)
    if new_city_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_city_dict['state_id'] = state_id

    new_city = City(**new_city_dict)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


