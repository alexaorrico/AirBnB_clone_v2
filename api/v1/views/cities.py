#!/usr/bin/python3

"""Defines City Route for rest API"""

from flask import request
from flask.helpers import abort
from flask.json import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities')
def get_state_cities(state_id):
    """Defines cities route in relation with state
    Args:
        state_id (str): state_id
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities]), 200


@app_views.route('/cities/<city_id>')
def get_city_by_id(city_id):
    """Defines cities route to retrieve city by id
        Args:
            city_id (str): id of city to retrive from storage
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', method=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """Route Delete a city based on the city id passed to url
    Args:
        city_id (str): city id to delete
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', method=['POST'])
def post_state_city(state_id):
    """Post a city to belong to state identified by its id
        Args:
            state_id (str): state id
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if not request.get_json().get('name'):
        abort(400, 'Missing Name')
    city = City(request.get_json())
    city.save()
    state.cities.append(city)
    return jsonify(city), 201
