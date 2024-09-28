#!/usr/bin/python3
"""
    This Module contains the routes for the CRUD
    for the cities
"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities', strict_slashes=True,
                 methods=['GET'])
def state_cities(state_id):
    """This Method Retrieves the list of all CIty Objects of a state"""
    cities = []
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    for city in state_obj.cities:
        cities.append(city.to_dict())
    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', strict_slashes=True, methods=['GET'])
def get_cities(city_id):
    """This Method Retrieves a city from the database based on the id"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict()), 200


@app_views.route('/cities/<city_id>', strict_slashes=True, methods=['DELETE'])
def delete_cities(city_id):
    """This Method Deletes a city object from the storage"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=True,
                 methods=['POST'])
def post_cities(state_id):
    """This Method creates a City"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    city_obj = City(state_id=state_id, **data)
    storage.new(city_obj)
    storage.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=True, methods=['PUT'])
def put_city(city_id):
    """This Method updates the data of a city"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
