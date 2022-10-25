#!/usr/bin/python3

"""Module to handle place request Blueprint"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """return json array of all places of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([val.to_dict() for val in places])


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new place"""
    if storage.get(City, city_id) is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in body:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, body["user_id"]) is None:
        abort(404)
    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)
    body["city_id"] = city_id
    new_place = Place(**body)
    new_place.save()
    if storage.get(Place, new_place.id) is not None:
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Method to get a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a single place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update properties of a single place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.get_json():
        body = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    _exceptions = ["id", "created_at", "updated_at", "city_id", "user_id"]
    for k, v in body.items():
        if k not in _exceptions:
            setattr(place, k, v)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
