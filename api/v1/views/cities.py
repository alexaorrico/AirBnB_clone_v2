#!/usr/bin/python3
""" Create a new view for cities and handle RESTFul API """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import Cities


@app_views.route('/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities():
    """ Gets the list of all City objects """
    cities = storage.all(City).values()
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ gits the states """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ why"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities', methods=['POST'],
                 strict_slashes=False)
def create_post():
    if request.is_json is False:
        abort(400, "Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    if request.is_json is False:
        abort(400, 'Not a JSON')
    data = request.get_json()
    cities = storage.all(City)
    s_key = "City." + city_id
    if s_key not in cities:
        abort(404)
    # Ignore keys: id, created_at, and updated_at
    ignored_keys = ['id', 'created_at', 'updated_at', 'city_id']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(cities[s_key], key, value)
    storage.save()
    return jsonify(cities[s_key].to_dict()), 200
