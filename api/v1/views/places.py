#!/usr/bin/python3
"""Handles all default RESTFUL API actions for places"""

from flask import abort, make_response, request, jsonify
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places_by_city_id(city_id):
    city = storage.get('City', city_id)
    """Get all places related to a city"""
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_places_by_id(place_id):
    """Get a place with the id"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Take an Id and delete a place identified by the id """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_city_place(city_id):
    """Takes a city id and post a place related to city"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, 'Missing user_id')
    user = storage.get('User', (request.get_json()).get('user_id'))
    if not user:
        abort(404)
    if "name" not in request.get_json():
        abort(400, "Missing name")
    place_data = request.get_json()
    place_data['city_id'] = city_id
    place = Place(**place_data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place identified by the place_id"""
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, val in request.get_json().items():
        if key not in ignore_keys:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
