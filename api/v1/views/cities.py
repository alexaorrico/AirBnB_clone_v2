#!/usr/bin/python3
""" New Funtion cities"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_all_cities(state_id):
    """Retrieves list of cities in a State"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    all_cities = storage.all("City").values()
    s_cities = [c.to_dict() for c in all_cities if c.state_id == state_id]
    return jsonify(s_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_city(city_id):
    """Retrieves city object """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_city(city_id):
    """Deletes city object """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Adds another object to the storage"""
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


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates an instance of City"""
    update_city_json = request.get_json(silent=True)
    if update_city_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, attr, val)
    storage.save()
    return jsonify(city.to_dict()), 200
