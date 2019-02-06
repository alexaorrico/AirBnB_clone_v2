#!/usr/bin/python3
"""Create a new view for City objects that handles all
default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def list_all_cities(state_id):
    """Retrieves a list of all Cities in a State"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    all_cities = storage.all("City").values()
    s_cities = [c.to_dict() for c in all_cities if c.state_id == state_id]
    return jsonify(s_cities)


@app_views.route('cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_a_city(city_id):
    """Retrieves a specific instance of City, otherwise 404 error"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_a_city(city_id):
    """Deletes a specific instance of City, otherwise 404 error"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Adds another object to the storage"""
    if not request.json:
        return {"error": "Not a JSON"}, 400
    elif 'name' not in request.json.keys():
        return {"error": "Missing name"}, 400
    new_city_dict = request.get_json()
    new_city_dict['state_id'] = state_id
    new_city = City(**new_city_dict)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates an instance of City"""
    if not request.json:
        return {'error': 'Not a JSON'}, 400
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    update_city_json = request.get_json()
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    for k, v in update_city_json.items():
        if k not in ignore:
            setattr(city, k, v)
    return jsonify(city.to_dict()), 200
