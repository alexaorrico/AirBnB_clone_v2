#!/usr/bin/python3
"""Defines the API routes for Place objects."""


from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
app = Flask(__name__)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")
    if "user_id" not in request_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, request_data["user_id"])
    if not user:
        abort(404)

    if "name" not in request_data:
        abort(400, description="Missing name")

    new_place = Place(**request_data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    request_data = request.get_json()
    if not request_data:
        abort(400, description="Not a JSON")

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
