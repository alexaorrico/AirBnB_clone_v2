#!/usr/bin/python3
"""Modules that handles all Restful API actions for Places"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_by_city(city_id):
    """Return a collection of places for a given city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Returns a given  object place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a given object place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a place resource"""
    new_city = storage.get(City, city_id)
    if new_city is None:
        abort(404)
    query = request.get_json()
    if not query:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in query:
        return jsonify({'error': 'Missing name'}), 400
    if 'user_id' not in query:
        return jsonify({'error': 'Missing user_id'}), 400
    else:
        user_id = query['user_id']
        user = storage.get(User, user_id)
        if user is None:
            abort(404)

    obj = Place(**query)
    setattr(obj, "city_id", city_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place with PUT method"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for attr, val in request.get_json().items():
        setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict()), 200
