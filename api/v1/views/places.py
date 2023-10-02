#!/usr/bin/python3
"""places view"""

from flask import Flask, jsonify, request, abort
from models import storage, Place, City, User

from api.v1.views import app_views

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve the list of all Place objects of a City by City ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    if "name" not in data:
        abort(400, "Missing name")

    new_place = Place(city_id=city_id, user_id=user_id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object by ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    # Remove keys that should be ignored
    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("city_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    for key, value in data.items():
        setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
