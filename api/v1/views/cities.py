#!/usr/bin/python3
""" Flask application that handle cities API"""
from models import storage
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Return list of cities in a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities_list = []
    for city in state.cities:
        city_dict = city.to_dict()
        cities_list.append(city_dict)
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieve a single city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Create a new city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    if 'name' not in json_obj:
        return jsonify("Missing name"), 400
    json_obj['state_id'] = state_id
    new_city = City(**json_obj)
    new_city.save()
    city = new_city.to_dict()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """Put a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    json_obj = request.get_json()
    if not request.json:
        return jsonify("Not a JSON"), 400
    ignore = ["id", "update_at", "created_at", "state_id"]
    for key, value in json_obj.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    new_city = city.to_dict()
    return jsonify(new_city), 200
