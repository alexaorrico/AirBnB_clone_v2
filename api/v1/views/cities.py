#!/usr/bin/python3
""" view for City objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_id():
    """Retrieves all State objects"""

    state_catch = storage.get(State, state_id)

    # If the state_id is not linked to any State object, raise a 404 error
    if state_catch is None:
        abort(404)


def cities():
    """Create a City"""
    if request.method == 'POST':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # If the dictionary doesn’t contain the key name
        if 'name' not in body_request_dict:
            abort(400, 'Missing name')

        # create new object State with body_request_dict
        new_city = City(**body_request_dict)

        storage.new(new_city)
        storage.save()
        return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_id():
    """Retrieves City object"""
    city_catch = storage.get(City, city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if city_catch is None:
        abort(404)

    # Retrieves a City object
    if request.method == 'GET':
        return city_catch.to_dict()

    # Deletes a City object
    if request.method == 'DELETE':
        empty_dict = {}
        storage.delete(city_catch)
        storage.save()
        return empty_dict, 200

    # update a City object
    if request.method == 'PUT':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # Update the City object with all key-value pairs of the dictionary
        # Ignore keys: id, state_id, created_at and updated_at

        for key, value in body_request_dict.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city_catch, key, value)

        city_catch.save()
        return city_catch.to_dict(), 200
