#!/usr/bin/python3
""" View for Cities  """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                  strict_slashes=False)
def get_cities_of_state(state_id):
    """ Return cities of a state"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    list_of_cities = []
    for city in state.cities:
        list_of_cities.append(city.to_dict())
    if list_of_cities:
        return jsonify(list_of_cities), 200
    else:
        return jsonify([]), 200


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cityby_id(city_id):
    """ Return a city based on city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """ Delete a city bases on city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ create new city """
    obj = request.get_json()
    if not obj:
        abort(400, "Not a JSON")
    if "name" not in obj:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    obj['state_id'] = state.id
    obj = City(**obj)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
        update an existing city
    """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for key, value in body.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
