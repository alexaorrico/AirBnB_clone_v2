#!/usr/bin/python3
""" City APIRest
 careful by default it uses get method
"""

from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities(state_id):
    """ list all cities from a state"""
    unique_state = storage.get("State", state_id)
    if not unique_state:
        abort(404)
    city_list = []
    for city in unique_state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)

@app_views.route('/cities/<city_id>', methods=['GET'])
def city_id(city_id):
    """ return the city
    """
    unique_city = storage.get("City", city_id)
    if not unique_city:
        abort(404)
    return jsonify(unique_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """ delete the delete
    """
    obj_to_delete = storage.get("City", city_id)
    if not obj_to_delete:
        abort(404)
    else:
        obj_to_delete.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """ create a city of a specified state
    """
    unique_state = storage.get("State", state_id)
    if not unique_state:
        abort(404)
    json_tmp = request.get_json()
    if not json_tmp:
        return jsonify("Not a JSON"), 400
    if 'name' not in json_tmp:
        return jsonify("Missing name"), 400
    new_city = City(**json_tmp, state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ update specified city
    """
    unique_city = storage.get("City", city_id)
    if not unique_city:
        abort(404)
    json_tmp = request.get_json()
    if not json_tmp:
        return jsonify("Not a JSON"), 400
    for key, value in json_tmp.items():
        if key == 'id' or key == 'updated_at' or key == 'created_at'\
           or key == 'state_id':
            pass
        setattr(unique_city, key, value)
    unique_city.save()
    return jsonify(unique_city.to_dict()), 200
