#!/usr/bin/python3
""" view for Place objects that handles all default RestFul API actions """
import os
import json
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def get_places(city_id=None):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=['GET'])
def get_place_id(place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def del_place_id(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def post_places(city_id):
    """ Creates a Place """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    my_request = request.get_json()
    if not my_request:
        abort(400, "Not a JSON")
    if "user_id" not in my_request:
        abort(400, "Missing user_id")
    user_id = my_request['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in my_request:
        abort(400, "Missing name")
    place = Place(**my_request)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'])
def put_place_id(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    my_request = request.get_json()
    if not my_request:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in my_request.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(pc.to_dict()), 200
