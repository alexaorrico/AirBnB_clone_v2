#!/usr/bin/python3
""" Places """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieve all places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a Place"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if 'user_id' not in payload:
        abort(400, "Missing user_id")
    user = storage.get(User, payload['user_id'])
    if not user:
        abort(404)
    if 'name' not in payload:
        abort(400, "Missing name")
    place = Place(city_id=city_id, **payload)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for key, value in payload.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
