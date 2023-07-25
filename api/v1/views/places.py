#!/usr/bin/python3
"""
places module that handles all default RESTful API
actions.
"""
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def place_all(city_id=None):
    """Returns all places or a place by specific ID"""
    if city_id:
        city = storage.get(City, city_id)
        if city is not None:
            placeList = [place.to_dict() for place in city.places]
            return jsonify(placeList)
        else:
            return abort(404)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id=None):
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
        else:
            return abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """deletes a place by ID"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """add place using POST"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    places = request.get_json()
    user = storage.get(User, places['user_id'])
    if user is None:
        abort(404)
    places['city_id'] = city_id
    newPlace = Place(**places)
    newPlace.save()
    return make_response(jsonify(newPlace.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update an place using PUT"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    notThese = ["id", "created_at", "updated_at", "city_id", "user_id"]
    for key, value in data.items():
        if key not in notThese:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
