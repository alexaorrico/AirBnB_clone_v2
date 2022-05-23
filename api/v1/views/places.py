#!/usr/bin/python3
""" view for City objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_city_id_places(city_id):
    """Retrieves all Place objects of a City"""

    city_catch = storage.get('City', city_id)

    # If the city_id is not linked to any City object, raise a 404 error
    if city_catch is None:
        abort(404)

    # retrieves Place object
    if request.method == 'GET':
        places = storage.all(Place)
        places_list = []
        for place in places.values():
            places_dict = place.to_dict()
            if places_dict['city_id'] == city_id:
                places_list.append(places_dict)
        return jsonify(places_list)

    elif request.method == 'POST':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # If the dictionary doesn’t contain the key user_id
        if 'user_id' not in body_request_dict:
            abort(400, 'Missing user_id')

        user_catch = storage.get('User', body_request_dict['user_id'])

        # If the user_id is not linked to any User object, raise a 404 error
        if user_catch is None:
            abort(404)

        # If the dictionary doesn’t contain the key name
        if 'name' not in body_request_dict:
            abort(400, 'Missing name')

        # create new object Place with body_request_dict
        body_request_dict['city_id'] = city_id
        new_place = Place(**body_request_dict)

        storage.new(new_place)
        storage.save()
        return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_id(place_id):
    """Retrieves Place object"""
    place_catch = storage.get(Place, place_id)

    # If the place_id is not linked to any Place object, raise a 404 error
    if place_catch is None:
        abort(404)

    # Retrieves a Place object
    if request.method == 'GET':
        return place_catch.to_dict()

    # Deletes a Place object
    if request.method == 'DELETE':
        empty_dict = {}
        storage.delete(place_catch)
        storage.save()
        return empty_dict, 200

    # update a Place object
    if request.method == 'PUT':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # Update the Place object with all key-value pairs of the dictionary
        # Ignore keys: id, state_id, created_at and updated_at

        for key, value in body_request_dict.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place_catch, key, value)

        place_catch.save()
        return place_catch.to_dict(), 200
