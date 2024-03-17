#!/usr/bin/python3
""" API views for Cities object(s)
Allows routes to list, get, delete, create, and update cities
as requested. """

from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Returns the list of all city objects of the passed state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Returns a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City in a State """
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, description="Not a JSON")
    if 'name' not in city_data:
        abort(400, description="Missing name")
    city = City(**city_data, state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """This deletes a state."""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    # Again, if you're here, you're an error.
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates the passed City object"""
    # Check if the Content-Type is application/json
    if request.content_type != 'application/json':
        abort(400,
              description="Invalid Content-Type. Expects 'application/json'")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, description="Not a JSON")
    for key, value in city_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
