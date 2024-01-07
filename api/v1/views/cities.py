#!/usr/bin/python3
""" cities.py """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                  methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Returns a JSON string"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                  methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns a JSON string"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                  methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Returns a JSON string"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                  methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Returns a JSON string"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                  methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Returns a JSON string"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.errorhandler(400)
def bad_request(error):
    """Returns a JSON string"""
    return jsonify({"error": "Not a JSON"}), 400


@app_views.errorhandler(404)
def not_found(error):
    """Returns a JSON string"""
    return jsonify({"error": 'Not found'}), 404
