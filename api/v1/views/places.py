#!/usr/bin/python3
"""handles all defaults RESTful API actions for places"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places():
    """retrieve all places"""
    city = storage.get(City, city_id)
    if city:
        places = storage.all(Place)
        places_list = []

    for place in places.values():
        places_list.append(place.to_dict())

    return jsonify(places_list)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """retrieves a place based on its id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    return abort(404)


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its id"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    return abort(404)
