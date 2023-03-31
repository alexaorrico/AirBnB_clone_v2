#!/bin/usr/python3
"""View of Cities for RESTFul API"""

from api.v1.views import app_views
from flask import jsonify, abort, Response
from models import storage

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
