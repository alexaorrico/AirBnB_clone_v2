#!/usr/bin/python3
"""
    API view related to City objects that handles all the default
    actions.
"""
from os import stat
import requests
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response, abort


def __is_valid_json(data):
    """
    Checks if the given data is a valid json.

    Args:
        data : Data to check

    Returns:
        True: If data is a valid json.
        False: If data is not a valid json.
    """
    try:
        json.loads(data)

        return True
    except Exception:
        return False


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_list(state_id) -> json:
    """
    Retrieves the list of all City objects.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Returns:
        json: List of City objects with status code 200.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    list = []
    for city in state.cities:
        list.append(city.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_show(city_id) -> json:
    """
    Retrieves a specified City object.

    Args:
        city_id : ID of the wanted City object.

    Raises:
        NotFound: Raises a 404 error if city_id
        is not linked to any City object.

    Returns:
        json: Wanted State object with status code 200.
    """
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id) -> json:
    """
    Deletes a specified City object.

    Args:
        city_id : ID of the wanted City object.

    Raises:
        NotFound: Raises a 404 error if city_id
        is not linked to any City object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def city_create(state_id) -> json:
    """
    Creates a new City object.

    Args:
        state_id : ID of the wanted State object.

    Raises:
        NotFound: Raises a 404 error if state_id
        is not linked to any State object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new State with the status code 201.
    """
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)

    if 'name' not in data.keys():
        return make_response('Missing name', 400)

    city = City(state_id=state_id)

    for key, value in data.items():
        if key is not "state_id":
            city.__setattr__(key, value)
    storage.new(city)
    storage.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def city_update(city_id) -> json:
    """
    Update a specified City object.

    Args:
        city_id : ID of the wanted City object.

    Returns:
        json: The updated City object with the status code 200.
    """
    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    for key, value in data.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            city.__setattr__(key, value)

    storage.new(city)
    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
