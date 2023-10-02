#!/usr/bin/python3
"""script to serve routes related to cities objects"""
from models.state import City
from models.state import State
from models import storage
from api.v1.views import app_views
import json
from flask import request, jsonify, abort

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves a list of all State objects"""
    cities = storage.all(City)
    list_cities = [city.to_dict() for city in cities.values() if city.state_id == state_id]

    if len(list_cities) == 0:
        abort(404)
    return jsonify(list_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def server_city_id(city_id):
    """Retrives a State object"""
    response = storage.get(City, city_id)

    if response is None:
        abort(404)

    return jsonify(response.to_dict())

@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city_obj(city_id):
    """deletes a State object"""
    city_to_delete = storage.get(City, city_id)

    if city_to_delete is None:
        abort(404)

    storage.delete(city_to_delete)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_new_city(state_id):
    """creates a State"""

    response = storage.get(State, state_id)

    if response is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    # if name not in dict
    if data_entered.get('name') is None:
        abort(400, description="Missing name")

    new_city = City(name=data_entered.get('name'))
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city_obj(city_id):
    """updates a State object"""
    city_to_update = storage.get(City, city_id)

    if city_to_update is None:
        abort(404)

    if request.headers['Content-Type'] == 'application/json':
        data_entered = request.get_json()
        if data_entered is None:
            # NOT WORKING NEEDS REPAIR !!!!!
            abort(400, description="Not a JSON")
    else:
        abort(400, description="Content-Type is not application/json")

    for key, value in data_entered.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city_to_update, key, value)

    storage.save()

    return jsonify(city_to_update.to_dict()), 200