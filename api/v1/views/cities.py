#!/usr/bin/python3

"""Defines City Route for rest API"""

from flask import request
from flask.helpers import abort, make_response
from flask.json import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.errorhandler(400)
def handle_400(e):
    """Error handler for 400"""
    return make_response(jsonify(error=str(e)), 400)


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_state_cities(state_id):
    """Defines cities route in relation with state
    Args:
        state_id (str): state_id
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities]), 200


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city_by_id(city_id):
    """Defines cities route to retrieve city by id
        Args:
            city_id (str): id of city to retrive from storage
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """Route Delete a city based on the city id passed to url
    Args:
        city_id (str): city id to delete
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
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
    city_data = request.get_json()
    city_data["state_id"] = state_id
    city = City(**city_data)
    city.save()
    return jsonify(city.to_dict()), 201


@ app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update a city from the city city_id selected"""
    city = storage.get('City', city_id)
    ignorekeys = ['id', 'state_id', 'created_at', 'update_at']
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, val in request.get_json().items():
        if key not in ignorekeys:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
