#!/usr/bin/python3
""" State objects RESTFul API. """
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getting_cities(state_id):
    """ Retrieves list of all State objs. """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    cities = [city.to_dict() for city in states.cities]
    return jsonify(cities)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """ Returns a state based from it's ID. """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes state based on id. """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def creates_a_city(state_id):
    """ Creates a City in a State. """
    state = storage.get(State, state_id)
    if not state:
        abort(404, 'State not found')
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'name' not in HTTP_body:
        abort(400, 'Missing name')
    city_data = request.get_json()
    city = City(name=city_data['name'], state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def updating_city(city_id):
    """ Updating a State obj. """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    ignoring_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in HTTP_body.items():
        if key not in ignoring_keys:
            setattr(cities, key, value)
    cities.save()
    return jsonify(cities.to_dict()), 200
