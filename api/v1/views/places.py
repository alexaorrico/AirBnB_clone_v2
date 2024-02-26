#!/usr/bin/python3
"""
places.py
"""
from . import app_views
from flask import jsonify
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, request, Response, make_response
import json


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def allplaces(city_id):
    """
    Retrieves the list of all place objects
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404, "try again")
    places_all = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            places_all.append(place.to_dict())
    return jsonify(places_all)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """
    retrieves one city per id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """
    retrieves one city per id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    creates place
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response("Missing name", 400)
    if 'user_id' not in data:
        return make_response("Missing user_id", 400)
    if not storage.get(User, data['user_id']):
        abort(404)
    new_place = Place(
        name=data["name"],
        city_id=city_id,
        user_id=data["user_id"])
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    updates city
    """
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    check = ["id", "created_at", "updated_at", "state_id"]
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for key, value in data.items():
        if key not in check:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
