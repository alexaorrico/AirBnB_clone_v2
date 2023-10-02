#!/usr/bin/python3
"""
    API module places
"""

import models
from models import storage
from models.place import *
from models.user import *
from models.city import *

from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """
        A function that Retrieves the list of all Place
        objects of a City: GET /api/v1/cities/<city_id>/places
    """
    # get city by id
    city = storage.get(City, city_id)

    # get places in city, save in list and return
    if (city):
        cityPlaces = [place.to_dict() for place in city.places]

        return jsonify(cityPlaces)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
        A function that Retrieves a Place object:
        GET /api/v1/places/<place_id>
    """
    # get place by id
    obj = storage.get(Place, place_id)

    # return place object dictionary if found
    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """
        A function that Deletes a Place object:
        DELETE /api/v1/places/<place_id>
    """
    # get place by id
    obj = storage.get(Place, place_id)

    # is place is found, delete object, save and return {}
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """
        A function that Creates a Place:
        POST /api/v1/cities/<city_id>/places
    """
    json_str = request.get_json()
    city = storage.get(City, city_id)

    if (city):

        # Error handling and missing info
        # Check If the HTTP body request is not valid JSON
        if (not json_str):
            abort(400, 'Not a JSON')
        if ('user_id' not in json_str):
            abort(400, 'Missing user_id')
        if ('name' not in json_str):
            abort(400, 'Missing name')

        user = storage.get(User, json_str['user_id'])
        if (not user):
            abort(404)

        json_str['city_id'] = city_id

        obj = Place(**json_str)

        obj.save()

        return jsonify(obj.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
        A function that Updates a Place object:
        PUT /api/v1/places/<place_id>
    """
    # get the place by id
    obj = storage.get(Place, place_id)

    if (obj):
        json_str = request.get_json()
        # Check If the HTTP body request is not valid JSON
        if (json_str is None):
            abort('400', 'Not a JSON')

        # Update Place objects attributes
        to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in json_str.items():
            if key not in to_ignore:
                setattr(obj, key, value)

        #  save and return
        obj.save()

        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
