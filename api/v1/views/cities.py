#!/usr/bin/python3
""" State objects RESTFul API. """
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getting_cities(state_id):
    """ Retrieves list of all State objs. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_by_id(city_id):
    """ Returns a state based from it's ID. """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes state based on id. """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def creates_a_city(state_id):
    """ Creates a City in a State. """
    state = storage.get(State, state_id)
    if not state:
        abort(404, description="State not found")
    cities = request.get_json(silent=True)
    if cities is None:
        abort(400, description="Not a JSON")
    if 'name' not in cities:
        abort(400, description="Missing name")
    city = City(name=cities['name'], state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def updating_city(city_id):
    """ Updating a State obj. """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    cities = request.get_json(silent=True)
    if cities is None:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in cities.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
