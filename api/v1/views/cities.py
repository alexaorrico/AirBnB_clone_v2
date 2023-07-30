#!/usr/bin/python3
"""
Module to handle all default RESTFul API actions for City objects.
"""
from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<str:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects related to the state with the \
        given state and returns them in JSON format.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities_list = [obj.to_dict() for obj in storage.all(City).values()
                   if obj.state_id == state_id]
    return jsonify(cities_list)


@app_views.route('/cities/<str:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves and returns City object with the given city_id.
    If not found, raise 404 error.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<str:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes City object with the given city_id.
    If not found, raise 404 error.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<str:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City and returns the new City with status code 201.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_city = City(name=request.get_json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/city/<str:city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates the city with the given city_id.
    Ignores id, created_at, updated_at keys.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city['name'] = request.get_json['name']
    storage.save()
    return jsonify(city.to_dict()), 200
