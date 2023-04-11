#!/usr/bin/python3
"""Places API routes"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_place_city(city_id):
    """Retrieves the list of all City Places objects"""
    city = storage.get(City, city_id)
    print(city)
    if city is None:
        abort(404)

    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    if 'user_id' not in req_json:
        abort(400, "Missing user_id")
    user = storage.get(User, req_json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in req_json:
        abort(400, "Missing name")
    req_json['city_id'] = city_id
    place = Place(**req_json)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route(
    '/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a User object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    ignore_key = ['id', 'user_id', 'city_id' 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore_key:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
