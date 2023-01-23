#!/usr/bin/python3
"""City API"""
from api.v1.views import app_views
from flask import*
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """get method for cities in a  state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all(City)
    state_city = []
    for city in cities.values():
        if city.state_id == state_id:
            state_city.append(city.to_dict())
    return jsonify(state_city)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Get a city from storage"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Create a city"""
    get_json = request.get_json()
    if get_json is None:
        abort(404, 'Not a JSON')
    if get_json['name'] is None:
        abort(404, 'Missing Name')

    get_json['state_id'] = state_id
    new_city = City(**get_json)
    new_city.save()
    return jsonify(new_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort('404')
    if request.get_json() is None:
        abort('404', 'Not a JSON')
    update = request.get_json()
    for key, value in update.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
