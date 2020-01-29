#!/usr/bin/python3
"""
    Module of blueprints of flask
"""
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def fetch_all_cities(state_id):
    """Fetch all states"""
    cities_list = []
    check_state = storage.get("State", state_id)
    if check_state is None:
        abort(404)
    cities = storage.all("City")
    for city in cities.values():
        if state_id == getattr(city, 'state_id'):
            cities_list.append(city.to_dict())
    return jsonify(cities_list), 200


@app_views.route("cities/<city_id>", methods=['GET'], strict_slashes=False)
def fetch_city(city_id):
    """Fetch a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a city"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, 'Not a JSON')
    if post_data.get('name') is None:
        abort(400, 'Missing name')
    check_state = storage.get("State", state_id)
    if check_state is None:
        abort(404)
    post_data['state_id'] = state_id
    new_city = City(**post_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a state"""
    attributes_unchanged = ['id', 'created_at',
                            'updated_at', 'state_id']
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(400, 'Not a JSON')
    for key, value in put_data.items():
        if key in attributes_unchanged:
            pass
        else:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
