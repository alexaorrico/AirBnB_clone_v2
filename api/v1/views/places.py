#!/usr/bin/python3
"""
Place objects API routes
"""

from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
        )
def get_places(city_id):
    """Retrieve the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False
        )
def create_place(city_id):
    """Create a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    new_place = Place(city_id=city_id, **data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400

    data = request.get_json()
    # Ignoring keys that should not be updated
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
