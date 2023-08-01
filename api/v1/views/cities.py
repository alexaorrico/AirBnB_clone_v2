#!/usr/bin/python3
""" new State object view. Handles default RESTful API actions"""
from flask import jsonify
from flask import abort
from api.v1.views import app_views
from models import storage
from flask import request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_city(state_id=None):
    """Get city by state id"""
    state = storage.get("State", state_id)
    if state_id is None or state is None:
        abort(404)
    else:
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id=None):
    """Get city by city id"""
    city = storage.get("City", city_id)
    if city_id is None or city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Deletes City objects based on given id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id=None):
    """Creates a City object based on get_json request"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    city = City()
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
            abort(400, 'Missing name')
    for key, value in data.items():
        setattr(city, key, value)
    setattr(city, "state_id", state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """Updates a City object based on id using response from get_json"""
    city = storage.get("City", city_id)
    data = request.get_json(silent=True)
    if city is None:
        abort(404)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
