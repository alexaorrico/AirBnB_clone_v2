#!/usr/bin/python3
"""Cities API actions"""

from flask import Flask, jsonify
from flask import abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/state/<state_id>", methods=["GET"], strict_slashes=False)
def get_cities_by_state(state_id):
    """retrieve a list of all cities"""
    state = storage.all("State", state_id)
    if not state:
        abort(404)
    result = city.to_dict()
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """CIty objects based on city id, else 404"""
    city = storage.get("City", city_id)
    if city:
        result = city.to_dict()
        return jsonify(result)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ CIty objects based on city id, else 404"""
    city = storage.get("City", city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<states_id>", methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """CIty objects based on state id, else 404"""
    city = request.get_json()
    if not city:
        abort(404)

    if "name" not in city:
        result = {"error": "Missing name"}
        return jsonify(result), 400

    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if 'name' not in new_city:
        abort(400, 'Missing name')
    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ CIty objects based on city id, else 404"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    update = request.get_json()
    if not update:
        result = {"error": "Not a JSON"}
        return jsonify(result), 400

    keys_to_exclude = ["id", "state_id", "created_at", "updated_at"]
    for key in keys_to_exclude:
        update.pop(key, None)

    for key, value in update.items():
        setattr(city, key, value)

    storage.save()
    city.save()
    result = city.to_dict()
    return jsonify(result), 200
