#!/usr/bin/python3
""" New view for cities object that handles all
default RESTFul API actions. """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_city_id(city_id):
    """ Retrieves, updates or deletes a city object given its id. """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in req_data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        storage.save()
        return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def state_cities(state_id):
    """ Retrieves all City objects of a state and creates
    a new city object in a state given the state's id.
    Returns 404 error if id is not found.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        list_cities = [city.to_dict() for city in state.cities]
        return jsonify(list_cities)

    if request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        if "name" not in req_data:
            abort(400, description="Missing name")

        req_data['state_id'] = state_id
        city = City(**req_data)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)
