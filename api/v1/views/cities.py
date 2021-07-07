#!/usr/bin/python3
"""This module is in charge of handling requests for state-type objects."""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities')
def cities_states(state_id):
    """return all city in states id"""
    all_cities = []
    for city in storage.all(City).values():
        if city.state_id == state_id:
            all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('states/<state_id>/cities', methods=['POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_id(city_id=None, state_id=None):
    """function that contains all the methods to perform in the api"""

    obj = storage.get(City, city_id)
    # Get a specific City object through the HTTP GET request.
    if request.method == 'GET':
        if obj is not None:
            return jsonify(obj.to_dict())
        abort(404)
    # Delete a specific City object through the HTTP DELETE request.
    elif request.method == 'DELETE':
        if obj is not None:
            storage.delete(obj)
            storage.save()
            return {}, 200
        abort(404)
    elif request.method == 'POST':
        obj_state = storage.get(State, state_id)
        if obj_state:
            if request.get_json(silent=True):
                if "name" in request.get_json(silent=True):
                    obj = City(**request.get_json(), state_id=state_id)
                    storage.new(obj)
                    storage.save()
                    return obj.to_dict(), 201
                return {"error": "Missing name"}, 400
            return {"error": "Not a JSON"}, 400
        abort(404)
    # Create a new City object through the HTTP POST request.
    elif request.method == 'POST':
        if request.get_json(silent=True):
            if "name" in request.get_json(silent=True):
                obj = State(**request.get_json())
                storage.new(obj)
                storage.save()
                return obj.to_dict(), 201
            return {"error": "Missing name"}, 400
        return {"error": "Not a JSON"}, 400
    # Update a specific City object through the HTTP PUT request.
    elif request.method == 'PUT':
        if obj is not None:
            if request.get_json(silent=True):
                fix_dict = request.get_json()
                attributes = ["id", "created_at", "updated_at"]
                for k, v in fix_dict.items():
                    if k not in attributes:
                        setattr(obj, k, v)
                obj.save()
                return obj.to_dict(), 200
            return {"error": "Not a JSON"}, 400
        abort(404)
