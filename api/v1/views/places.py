#!/usr/bin/python3
"""
a new view for Place objects that handles
all default RESTFul API actions:
"""
import json
from api.v1.views import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from flask import Flask, make_response, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_places(city_id):
    """
    he list of all Place objects of a City:

    Args:
        city_id : ID of the specified City object.

    Raises:
        NotFound: Raises a 404 error if city_id
        is not linked to any User object.

    Returns:
        json: Wanted Place object with status code 200.
    """
    city = storage.all(City, city_id)
    place_list = []

    if city is None:
        raise NotFound

    places = city.places

    for place in places.items():
        place_list.append(place.to__dict())
    return make_response(jsonify(place_list), 200)


@app_views.route('/places/<place_id>', methods=['GET'])
def single_place(place_id):
    """
    Retrieves a specified Placeobject.

    Args:
        place_id : ID of the specified Place object.

    Raises:
        NotFound: Raises a 404 error if place_id
        is not linked to any Place object.

    Returns:
        json: Wanted Place object with status code 200.
    """
    place = storage.get(Place, place_id)

    if place is None:
        raise NotFound

    return make_response(jsonify(place.to__dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
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


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """
    Creates a new Place object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new Place with the status code 201.
    """
    city = storage.get(City, city_id)

    if city is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json().keys():
        return make_response('Missing name', 400)

    if 'user_id' not in request.get_json().keys():
        return make_response('Missing user_id', 400)

    user = storage.get(User, request.get_json()['user_id'])

    if user is None:
        raise NotFound

    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)

    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Update a specified  Place object.

    Args:
        user_id : Id of the wanted A Place object.

    Returns:
        json: The updated Placey object with the status code 200.
    """
    place = storage.get(Place, place_id)

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if place is None:
        raise NotFound

    for key, plac in request.get_json().items():
        if key not in ('id', 'created_at', 'updated_at'):
            place.__setattr__(key, plac)

    place.save()

    return make_response(jsonify(place.to__dict()), 200)
