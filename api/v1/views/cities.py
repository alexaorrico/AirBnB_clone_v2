#!/usr/bin/python3
"""
This is the cities page endpoints
"""

from api.v1.views import app_views
from flask import jsonify, request
from werkzeug.exceptions import NotFound
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def fetch_states_cities(state_id=None):
    """Fetches all cities for a state from the database"""
    state = storage.get(State, state_id)
    if not state:
        raise NotFound
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_city(city_id):
    """Fetches a city obj using the city id"""
    cities = storage.all(City)
    if city_id:
        for city in cities.values():
            if city.id == city_id:
                return jsonify(city.to_dict())
    raise NotFound


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city obj using the city id"""
    cities = storage.all(City)
    if city_id:
        for city in cities.values():
            if city.id == city_id:
                storage.delete(city)
                storage.save()
                return jsonify({}), 200
    raise NotFound


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city and saves it to the db"""
    state = storage.get(State, state_id)
    if not state:
        raise NotFound
    city = request.get_json()
    if not city:
        return jsonify(error='Not a JSON'), 400
    if 'name' not in city:
        return jsonify(error='Missing name'), 400
    city = City(**city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """This method updates a city's data"""
    city = storage.get(City, city_id)
    if not city:
        raise NotFound
    new_city = request.get_json()
    if not new_city:
        return jsonify(error='Not a JSON'), 400

    for key, value in new_city.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
