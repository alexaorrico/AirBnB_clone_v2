#!/usr/bin/python3
"""
This module contains the views for City objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_state(state_id):
    """retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities
              if city.state_id == state_id]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """retrieves a City object using its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """deletes a State object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a new City object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, "Not a JSON")
    if not data.get('name'):
        abort(400, "Missing name")
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    data.update({'state_id': state_id})
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())
