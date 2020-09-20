#!/usr/bin/python3
"""
view for Place objects that handles all default RestFul API action
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


# the followings are the entendpoints of the app_view blueprint
# in other words /status == /api/v1/status and /stats == /api/v1/stats
# we create that blueprint to access to all the endpoints easily

@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_all(city_id):
    """ returns list of all Place objects linked to a given City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description="city_id not linked to any City object")
    places_all = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            places_all.append(place.to_dict())
    return jsonify(places_all)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_get(place_id):
    """ handles GET method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="place_id not linked to any Place object")
    place = place.to_dict()
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ handles DELETE method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="place_id not linked to any Place object")
    storage.delete(place)
    storage.save()
    response = make_response(jsonify({}), 200)
    return response


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """ handles POST method """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description="city_id not linked to any City object")
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404, description="user_id not linked to any User object")
    if 'name' not in data.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_place = Place(**data)
    new_place.city_id = city_id
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id):
    """ handles PUT method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="city_id not linked to any City object")
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
