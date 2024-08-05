#!/usr/bin/python3
"""
Module to handle API endpoints related to Place objects.
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Retrieve all places within a specific city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description="City not found")
    response = [place.to_dict() for place in city.places]
    return jsonify(response)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id=None):
    """Get detailed information about a specific place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id=None):
    """Remove a place from the database."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Add a new place to a specific city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description="City not found")
    body = request.get_json()
    if not body or not isinstance(body, dict):
        abort(400, description="Not a JSON")
    if 'name' not in body:
        abort(400, description="Missing name")
    if 'user_id' not in body:
        abort(400, description="Missing user_id")
    if storage.get(User, body['user_id']) is None:
        abort(404, description="User not found")
    body['city_id'] = city_id
    new_place = Place(**body)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """Modify an existing place with new data."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")
    new_data = request.get_json()
    if not new_data or not isinstance(new_data, dict):
        abort(400, description="Not a JSON")
    for key in new_data:
        if key not in ['id', 'created_at', 'city_id', 'user_id', 'updated_at']:
            setattr(place, key, new_data[key])
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
