#!/usr/bin/python3
"""
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.state import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cites_id(state_id=None):
    """
    """
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    cities = storage.all("City")
    cities_ = [i.to_dict() for i in cities.values()
                       if i.state_id == state_id]
    return (jsonify(cities_))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city(city_id=None):
    """
    """
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_del(city_id=None):
    """
    """
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    cities.delete()
    cities.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_id(state_id=None):
    """
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    dic = request.get_json()
    dic.update({'state_id': state_id})
    instance = City(**dic)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/cities/<cities_id>', methods=['PUT'], strict_slashes=False)
def city_update(cities_id):
    """
    """
    key = ['id', 'created_at', 'updated_at', 'state_id']
    city = storage.get('City', cities_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for keys, value in request.get_json().items():
        if keys in key:
            pass
        else:
            setattr(city, keys, value)
    city.save()
    return jsonify(city.to_dict()), 200
