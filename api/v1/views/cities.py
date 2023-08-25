#!/usr/bin/python3
"""
Module City
"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_from_state(state_id):
    """
    Retrives list of all cities by id
    """
    # get data
    state = storage.get(State, state_id)
    # if id not linked to state, error 404
    if state is None:
        abort(404)
    # store each city
    all_cities = [city.to_dict() for city in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities_by_name(city_id=None):
    """
    Display city object by name
    """
    # get data
    city_obj = storage.get(City, city_id)
    # if id not linked to city, error 404
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a city
    """
    # get data
    delete_city = storage.get(City, city_id)
    # if id not linked to city, error 404
    if delete_city is None:
        abort(404)
    else:
        # deletes city at id, saves and returns status 200
        delete_city.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    Creates a state object
    """
    # parses incoming json file
    posted = request.get_json()
    # returns error message and status 400 if not a json file
    if posted is None:
        return jsonify({'error': 'Not a JSON'}), 400
    # gets the state linked to state_id
    state = storage.get(State, state_id)
    # if state_id not linked to a state status error 404
    if state is None:
        abort(404)
    # returns error message and status 400 if no key 'name'
    if 'name' not in posted:
        return jsonify({'error': 'Missing name'}), 400

    if type(posted) is dict:
        posted['state_id'] = state_id
        # gets, creates, saves and returns the new city with code 201
        obj = City(**posted)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updates_cities_id(city_id):
    """
    Updates state object
    """
    # parses incoming json file
    updates_city = request.get_json()
    # returns error message and status 400 if not a json file
    if updates_city is None:
        return jsonify({'error': 'Not a JSON'}), 400
    # gets the city linked to city_id
    city = storage.get(City, city_id)
    # if city_id not linked to a city status error 404
    if city is None:
        abort(404)
    else:
        # sets ignored keys
        ignore = ['id', 'state_at', 'created_at' 'updated_at']
        # updates the city with all-value pairs of dict
        for key, value in updates_city.items():
            if key not in ignore:
                setattr(city, key, value)
            else:
                pass
        # saves and returns object with status 200
        storage.save()
        return jsonify(city.to_dict()), 200
