#!/usr/bin/python3
"""Flask application that handle cities API"""
from flask import jsonify, abort, request
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
   """Return list of cities in a state"""
    unique_state = storage.get("State", state_id)
    if not unique_state:
        abort(404)
    city_list = []
    for city in unique_state.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def get_cities_id(city_id):
    """Return a single city"""
    if request.method == 'GET':
        unique_city = storage.get("City", city_id)
        if not unique_city:
            abort(404)
        return jsonify(unique_city.to_dict())
    elif request.method == 'DELETE':
        obj_to_delete = storage.get("City", city_id)
        if not obj_to_delete:
            abort(404)
        else:
            obj_to_delete.delete()
            storage.save()
            return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Post new city"""
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


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Put method to update city"""
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
