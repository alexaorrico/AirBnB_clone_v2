#!/usr/bin/python3
"""Flask route for city model"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/cities/<city_id>", methods=['GET'])
def city_no(city_id):
    """route to return all cities"""
    city_obj = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def city_del(city_id):
    """ del city"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def create_new(state_id):
    """ create new city"""
    newState = storage.get_json()
    if newState is None:
        abort(404)
        request_json = request.get_json()
        if not request_json:
            abort(404, "Not a JSON")
            if "name" not in request_json:
                abort(404, "Missing name")
            newCity = City(state_id=state.id, **request_json)
            newCity.save()
            return jsonify(newCity.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def city_update(state_id):
    """Get, update city"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(400)
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")
        city_obj.name = request_json.get("name", city_obj.name)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
