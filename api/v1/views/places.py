#!/usr/bin/python3
"""amenity
Module to create view for Place objects handling default
RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=["GET"])
def places_get(city_id=None):
    """
    Retrieves list of all Place objects linked to a City.
    """
    if city_id:
        city = storage.get(City, city_id)
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    else:
        return abort(404)


@app_views.route("/places/<string:place_id>", methods=["GET"])
def place_id_get(place_id):
    """
    Retrieves an place with a given id
    Raise 404 error if id not linked to any Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"])
def place_id_delete(place_id):
    """
    Deletes an Place object with a given id
    Raise 404 error if id not linked to any Place object
    Returns and empty dictionary with status code 200
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<string:city_id>/places/", methods=["POST"])
def place_post(city_id):
    """
    Creates an Place via POST
    If the HTTP body request is not valid JSON, raise 400 error, Not a JSON
    If the dictionary doesn't contain the key name, raise a 400 error with
    message Missing name
    Returns new Place with status code 201
    """
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    places_kwargs = request.get_json()
    if "user_id" not in places_kwargs:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if "name" not in places_kwargs:
        return make_response(jsonify({"error": "Missing name"}), 400)
    user = storage.get(User, places_kwargs["user_id"])
    if user is None:
        return abort(404)
    else:
        Place["cities_id"] = city_id
        new_place = Place(**places_kwargs)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)

@app_views.route("/place/<string:place_id>", methods=["PUT"])
def place_put(state_id):
    """
    Updates an Place object via PUT
    If the place_id is not linked to any Place object, raise 404 error
    If the HTTP body request is not valid JSON, raise a 400 error, Not a JSON
    Update the Place object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    """
    place = storage.get(Place, state_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
