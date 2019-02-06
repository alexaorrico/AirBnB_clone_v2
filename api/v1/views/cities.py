#!/usr/bin/python3
""" module that handles all default RestFul API actions
"""

from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities_by_state(state_id):
    """ get all city objects given a state"""
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    city_objs = obj.cities
    return jsonify([city.to_dict() for city in city_objs])


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """ get state object """
    obj = storage.get("City", city_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """delete state object"""
    obj = storage.get("City", city_id)
    if obj:
        obj.delete()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """create state instance"""
    request_dict = request.get_json()
    if not request_dict:
        abort(400, {"message": "Not a JSON"})
    if "name" not in request_dict:
        abort(400, {"message": "Missing name"})
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    obj = City(**request_dict)
    obj.state_id = state_id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def put_city(city_id):
    """update state object"""
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    request_dict = request.get_json()
    if not request_dict:
        abort(400, {"message": "Not a JSON"})
    for key, value in request_dict.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    return jsonify(obj.to_dict()), 200
