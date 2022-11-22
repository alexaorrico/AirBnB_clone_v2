#!/usr/bin/python3
"""view for Place objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models import storage
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def place(city_id):
    """retrieves the list of places objects of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    plas = []
    for place in city.places:
        plas.append(place.to_dict())
    return jsonify(plas)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieves a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/place/<place_id>', methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """deletes an instance of plate"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """creates a place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user_id = data['user_id']
    if not storage.get(User, user_id):
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")

    data['city_id'] = city_id
    place = Place(**data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """update the place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, values in data.items():
        if key not in ['id', 'user_id', 'city_id', "created_at", 'updated_at']:
            setattr(place, key, values)
    storage.save()
    return jsonify(place.to_dict()), 200
