#!/usr/bin/python3
"""city.py"""

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False)
def get_cities_of_state(state_id=None):
    """retrieves all cities """
    if storage.get(State, state_id) is None:
        abort(404)

    cities_obj = storage.all(City)

    cities = []
    for city in cities_obj.values():
        if city.to_dict().get('state_id') == state_id:
            cities.append(city.to_dict())
    # or we can do
    # cities = [city.to_dict() for city in cities_obj.values()
    # if city.to_dict().get('state_id') == state_id]

    return jsonify(cities), 200


@app_views.route("/cities/<string:city_id>")
def get_city(city_id=None):
    """retrieves a specific city """
    if city_id is None:
        abort(404)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'])
def delete_city(city_id=None):
    """retrieves a specific city """
    if city_id is None:
        abort(404)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route(
        "/states/<string:state_id>/cities",
        methods=['POST'],
        strict_slashes=False)
def create_city(state_id=None):
    """ Creates a city"""
    if storage.get(State, state_id) is None:
        return jsonify({"error": "Not found"}), 404

    city_dict = None
    try:
        city_dict = request.get_json()
        if not isinstance(city_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in city_dict:
        return jsonify({"error": "Missing name"}), 400

    city = City(name=city_dict['name'], state_id=state_id)
    storage.new(city)
    storage.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """ updates a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city_dict = None
    try:
        city_dict = request.get_json()
        if not isinstance(city_dict, dict):
            raise ValueError
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    for key, val in city_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, val)

    storage.save()
    return jsonify(city.to_dict()), 200
