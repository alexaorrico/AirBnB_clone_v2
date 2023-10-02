#!/usr/bin/python3
"""Defines views for cities module"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    """Retrieves a dict of cities of a state.
        methods::
                - GET: retrieve specified state.
                - POST: Creates new specified state
    """
    if request.method == 'GET':
        state = storage.get('State', state_id)
        if state is None:
            abort(404)
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get('name') is None:
            abort(400, 'Missing name')
        city = City(**data)
        setattr(city, 'state_id', state_id)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves, Deletes or Updates a city object by it's id
        methods::
                - GET: retrieve specified city.
                - PUT: Updates specified city with info
                - DELETE: Deletes specified city instance
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        data = request.get_json()
        if data in None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in {'created_at', 'updated_at', 'id', 'state_id'}:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())
