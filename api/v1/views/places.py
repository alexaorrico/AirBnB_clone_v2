#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, City, User, Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    data = request.get_json
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    user_id = data['user_id']
    if storage.get(User, user_id) is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    data = request.get_json
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
