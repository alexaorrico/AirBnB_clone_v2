#!/usr/bin/python3
""" This module contains the cities view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_cities(state_id=None):
    """ Retrieves the list of all City objects of a State """
    state = storage.get('State', state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])
    elif request.method == 'POST':
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        if 'name' not in req_json:
            abort(400, 'Missing name')
        city = City(**req_json)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_city(city_id=None):
    """ Retrieves a City object """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
