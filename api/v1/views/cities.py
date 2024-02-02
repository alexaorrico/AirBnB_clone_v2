#!/usr/bin/python3
"""
A view for City objects that handles all default RESTFul API Actions
"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_of_state(state_id):
    """ This route retrieves all the cities of a certain state """
    state = storage.get(State, state_id)
    # Checking if the state exists
    if state is None:
        abort(404)
    cities_obj = state.cities
    # Action for GET method
    if request.method == 'GET':
        cities = []
        for obj in cities_obj:
            cities.append(obj.to_dict())
        return jsonify(cities)
    # Action for POST method
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city_by_id(city_id):
    """ Retrieve city by corresponding id """
    city = storage.get(City, city_id)
    # Check if the city exists
    if city is None:
        abort(404)
    # Action for GET method
    if request.method == 'GET':
        return jsonify(city.to_dict())
    # Action for DELETE method
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    # Action for PUT method
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'created_at', 'updated_at', 'state_id']
    for key in data.keys():
        if key not in ignore_keys:
            setattr(city, key, data[key])
    storage.save()
    return jsonify(city.to_dict()), 200
