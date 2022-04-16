#!/usr/bin/python3
"""city"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id=None):
    """all City"""
    all_cities = []
    state_obj = storage.get("State", state_id)
    if state_obj:
        for city_obj in state_obj.cities:
            all_cities.append(city_obj.to_dict())
        return jsonify(all_cities)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """City object"""
    city_obj = storage.get("City", city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """deletes a City object"""
    city_obj = storage.get("City", city_id)
    if city_obj:
        storage.delete(city_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city object"""
    state_obj = storage.get("State", state_id)
    obj_request = request.get_json()
    if state_obj:
        if obj_request:
            if 'name' in obj_request:
                new_city_obj = City(**obj_request)
                setattr(new_city_obj, "state_id", state_id)
                new_city_obj.save()
                return (jsonify(new_city_obj.to_dict()), 201)
            else:
                return "Missing name", 400
        else:
            return "Not a JSON", 400
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def updates_city(city_id):
    """updates a city object"""
    city_obj = storage.get("City", city_id)
    obj_request = request.get_json()
    if city_obj:
        if obj_request:
            if 'name' in obj_request:
                for key, value in obj_request.items():
                    ignore = ["id", "state_id", "created_at", "updated_at"]
                    if key != ignore:
                        setattr(city_obj, key, value)
                city_obj.save()
                return jsonify(city_obj.to_dict())
            else:
                return "Missing name", 400
        else:
            return "Not a JSON", 400
    else:
        abort(404)
