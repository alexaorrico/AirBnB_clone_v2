#!/usr/bin/python3
"""objects that handle all default RestFul API actions for Reviews"""

from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False)
def get_places(city_id):
    """Method for list all places from city"""
    new_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route("/places/<string:place_id>", strict_slashes=False)
def one_place(place_id):
    """Method for list one place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_delete(place_id):
    """Method that deletes a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """Method that creates a place"""
    city = storage.get(City, city_id)
    data = request.get_json()
    if not city:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id):
    """Method that puts a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
