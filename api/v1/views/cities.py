#!/usr/bin/python3
"""
text
"""
from models import storage
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def get_or_create_city(state_id):
    """Get cities by state or create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    elif request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')

        data = request.get_json()
        name = data.get('name')
        if not name:
            abort(400, 'Missing name')

        new_city = City(**data)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_update_or_delete_city(city_id):
    """Get, update, or delete a city by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        if not request.is_json:
            abort(400, 'Not a JSON')

        data = request.get_json()
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
