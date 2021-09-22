#!/usr/bin/python3
"""Module for actions and handles Apparently needs to be more documented."""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.state import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(city_id):
    """retrieves the list of all city objects"""
    cities = []
    for value in storage.all("City").values():
        cities.append(value.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """retrieves a city object"""
    cities_dic = storage.get("City", city_id)
    if cities_dic is None:
        abort(404)
    return jsonify(cities_dic.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city_del = storage.get("City", city_id)
    if city_del is None:
        abort(404)
    city_del.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def createCity():
    """Creates a new City"""
    if request.get_json() is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = City(**request.get_json())
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/states/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a city obj"""
    if not request.get_json():
        make_response(jsonify({'error': 'Not a JSON'}), 400)

    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()
    return jsonify(obj.to_dict())
