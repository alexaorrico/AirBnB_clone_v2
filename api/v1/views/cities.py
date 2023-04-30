#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """
    Retrieve the list of all cities
    """
    states = storage.all(State).values()
    if states is None:
        abort(404)
    return jsonify([city.to_dict() for city in states.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id=None):
    """
    Retrieve the state by id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """
    Delete state with the diven id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create a new state from the json request
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.is_json()
    if 'name' not in data:
        abort(400, "Missing name")
    city = City(name=data['name'], city_id=city_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Update the state of the given id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
