#!/usr/bin/python3
"""
    API view related to Place objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response


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


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_list(city_id) -> json:
    """
    Retrieves the list of all Place objects.

    Returns:
        json: List of Place objects with status code 200.
    """
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    places = city.places

    list = []
    for place in places:
        list.append(place.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/places/<place_id>', methods=['GET'])
def place_show(place_id) -> json:
    """
    Retrieves a specified Place object.

    Args:
        place_id : ID of the wanted Place object.

    Raises:
        NotFound: Raises a 404 error if place_id
        is not linked to any Place object.

    Returns:
        json: Wanted Place object with status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id) -> json:
    """
    Deletes a specified Place object.

    Args:
        place_id : ID of the wanted Place object.

    Raises:
        NotFound: Raises a 404 error if place_id
        is not linked to any Place object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def place_create(city_id) -> json:
    """
    Creates a new Place object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'email' or 'password'
        is not present sends status code 400.

    Returns:
        json: The new Place with the status code 201.
    """
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)

    if 'name' not in data.keys():
        return make_response('Missing name', 400)

    if 'user_id' not in data.keys():
        return make_response('Missing user_id', 400)

    place = Place()
    place.city_id = city_id

    for key, value in data.items():
        if key != "city_id":
            place.__setattr__(key, value)

    storage.new(place)
    storage.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_update(place_id) -> json:
    """
    Update a specified Place object.

    Args:
        state_id : Id of the wanted State object.

    Returns:
        json: The updated State object with the status code 200.
    """
    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    for key, value in data.items():
        if key not in ('id', 'city_id', 'created_at', 'updated_at'):
            place.__setattr__(key, value)

    storage.new(place)
    storage.save()

    return make_response(jsonify(place.to_dict()), 200)
