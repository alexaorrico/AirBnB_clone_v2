#!/usr/bin/python3
"""
Views for City
"""
from flask import request, abort, jsonify
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities(state_id=None):
    """
    Retrieves the list of all City objects: GET /api/v1/cities
    Creates a City: POST /api/v1/cities
    """
    if request.method == 'GET':
        list_cities = []
        state = storage.get('State', state_id)
        for city in state.cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities), 200

    if request.method == 'POST':
        request_json = request.get_json()
        if not request_json:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in request_json:
            return jsonify({'error': 'Missing name'}), 400
        state = storage.get('State', state_id)
        if state:
            request_json['state_id'] = state_id
            city = City(**request_json)
            storage.new(city)
            storage.save()
            return jsonify(city.to_dict()), 200
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def city(city_id=None):
    """
    Retrieves the list of all City objects: GET /api/v1/cities
    Creates a City: POST /api/v1/cities
    """
    if request.method == 'GET':
        city = storage.get('City', city_id)
        if city:
            return jsonify(city.to_dict()), 200
        abort(404)

    if request.method == 'DELETE':
        city = storage.get('City', city_id)
        if city:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        abort(404)

    if request.method == 'PUT':
        request_json = request.get_json()
        if not request_json:
            return jsonify(error='Not a JSON'), 200
        city = storage.get('City', city_id)
        if city:
            for key, value in request_json.items():
                if key not in ["__class__", "id", "created_at", "updated_at"]:
                    setattr(city, key, value)
            storage.save()
            return jsonify(city.to_dict()), 200
        abort(404)
