#!/usr/bin/python3
"""Cities API actions"""

from flask import Flask, jsonify
from flask import abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/cities", strict_slashes=False)
def all_cities():
    """retrieve a list of all cities"""
    cities = storage.all("City")
    all_cities = [city.to_dict() for city in cities.values()]
    return jsonify(all_cities), 200


@app_views.route("/cities/<city_id>", methods=['GET'])
def city_by_id(city_id):
    """CIty objects based on city id, else 404"""
    city = storage.get("City", city_id)
    if city:
        result = city.to_dict()
        return jsonify(result), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """ CIty objects based on city id, else 404"""
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['POST'])
def create_city(state_id):
    """CIty objects based on state id, else 404"""
    city = request.get_json()
    if not city:
        result = {"error": "Not a JSON"}
        return jsonify(result), 400
    if "name" not in city:
        result = {"error": "Missing name"}
        return jsonify(result), 400
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    city_name = city.get("name")
    existing_cities = [city for city in state.cities
                       if city.name == city_name]
    if existing_cities:
        existing_city = existing_cities[0]
        for key, value in city.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(existing_city, key, value)
        existing_city.save()
        result = existing_city.to_dict()
        return jsonify(), 200

    new_city = City(state_id=state_id, **city)
    new_city.save()
    result = new_city.to_dict()
    return jsonify(result), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
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

    city.save()
    result = city.to_dict()
    return jsonify(result), 200
