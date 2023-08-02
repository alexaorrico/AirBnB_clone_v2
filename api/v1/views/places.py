#!/usr/bin/python3
"""
View for Places that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_all(city_id):
    """ returns list of all Place objects linked to a given City """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_all = []
    places = storage.all("Place").values()
    for place in places:
        if place.city_id == city_id:
            places_all.append(place.to_json())
    return jsonify(places_all)


@app_views.route('/places/<place_id>', methods=['GET'])
def place_get(place_id):
    """ handles GET method """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place = place.to_json()
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """ handles DELETE method """
    empty_dict = {}
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """ handles POST method """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data.keys():
        abort(400, "Missing name")
    place = Place(**data)
    place.city_id = city_id
    place.save()
    place = place.to_json()
    return jsonify(place), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_put(place_id):
    """ handles PUT method """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            place.bm_update(key, value)
    place.save()
    place = place.to_json()
    return jsonify(place), 200
