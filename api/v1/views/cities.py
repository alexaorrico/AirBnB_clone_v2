#!/usr/bin/python3
"""
API endpoints for City objects.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_state(state_id):
    """Retrieves the list of all City objects of a State"""
    list_city = []
    for city in storage.all(City).values():
        if state_id == city.id:
            list_city.append(city.to_dict())
    if not list_city:
        abort(404)
    return jsonify(list_city)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object. : GET /api/v1/cities/<city_id>
    If the city_id is not linked to any City object, raise a 404 error
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    city_data = request.get_json()
    if city_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in city_data:
        abort(400, 'Missing name')
    new_city = City(name=city_data['name'], state_id=state.id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city_data = request.get_json()
    if city_data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in city_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
