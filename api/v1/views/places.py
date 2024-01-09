#!/usr/bin/python3
"""
This is the places page endpoints
"""

from api.v1.views import app_views
from flask import jsonify, request
from werkzeug.exceptions import NotFound
from models import storage
from models.place import Place
from models.user import User


@app_views.route('/cities/<place_id>/places', methods=['GET'],
                 strict_slashes=False)
def fetch_cities_places(place_id=None):
    """Fetches all places for a place from the database"""
    place = storage.get(place, place_id)
    if not place:
        raise NotFound
    return jsonify([place.to_dict() for place in place.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_place(place_id):
    """Fetches a place obj using the place id"""
    places = storage.all(place)
    if place_id:
        for place in places.values():
            if place.id == place_id:
                return jsonify(place.to_dict())
    raise NotFound


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place obj using the place id"""
    places = storage.all(place)
    if place_id:
        for place in places.values():
            if place.id == place_id:
                storage.delete(place)
                storage.save()
                return jsonify({}), 200
    raise NotFound


@app_views.route('/cities/<place_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(place_id):
    """Creates a new place and saves it to the db"""
    place = storage.get(place, place_id)
    if not place:
        raise NotFound
    place = request.get_json()
    if not place:
        return jsonify(error='Not a JSON'), 400
    if 'user_id' not in place:
        return jsonify(error='Missing user_id')
    user = storage.get(User, place['user_id'])
    if not user:
        raise NotFound
    if 'name' not in place:
        return jsonify(error='Missing name'), 400
    place = Place(**place)
    setattr(place, 'place_id', place_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """This method updates a place's data"""
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound
    new_place = request.get_json()
    if not new_place:
        return jsonify(error='Not a JSON'), 400

    for key, value in new_place.items():
        if key not in ['id', 'user_id', 'user_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
