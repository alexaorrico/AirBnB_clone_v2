#!/usr/bin/python3
"""City API"""
from api.v1.views import app_views
from flask import *
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_cities(state_id):
    """get method for cities in a  state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        cities = storage.all(City)
        return jsonify([city.to_dict() for city in cities.values()
                        if city.to_dict().get("state_id") == state_id])
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if data.get("name") is None:
            abort(400, "Missing name")
        data["state_id"] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_city(city_id):
    """Get a city from storage"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(
            city.to_dict()
        )
    if request.method == 'DELETE':
        city.delete()
        del city
        return jsonify({}), 200
    if request.method == 'PUT':
        update = request.get_json()
        if update is None:
            abort(400, 'Not a JSON')
        for key, val in update.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict()), 200
