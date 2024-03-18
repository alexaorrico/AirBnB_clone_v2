#!/usr/bin/python3
""" State objects RESTFul API. """
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getting_states():
    """ Retrieves list of all State objs. """
    states = storage.all(State).values()
    list_of_states = [state.to_dict() for state in states]
    return jsonify(list_of_states)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(state_id):
    """ Returns a state based from it's ID. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(city_id):
    """ Deletes state based on id. """
    state = storage.get(City, city_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def creates_a_city(state_id):
    """ Creates a City in a State. """
    if not storage.get(State, state_id):
        abort(404, 'State not found')
    HTTP_body = request.get_json(silent=True)
    if not HTTP_body:
        abort(400, 'Not a JSON')
    if 'name' not in HTTP_body:
        abort(400, 'Missing name')
    HTTP_body['state_id'] = state_id
    latest_city = City(**HTTP_body)
    storage.new(latest_city)
    storage.save()
    return jsonify(latest_city.to_dict()), 201


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
    storage.save()
    return jsonify(cities.to_dict()), 200
