#!/usr/bin/python3
"""Defines all the places routes"""

from flask import jsonify, request, abort
from api.v1.views import place_view
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@place_view.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_city_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = storage.all(Place).values()
    city_places = [place.to_dict() for place in places if place.city_id == city_id]

    return jsonify(city_places)


@place_view.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@place_view.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)
    place.delete()
    storage.save()

    return jsonify({}), 200


@place_view.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    user_id = data.get('user_id')
    if user_id is None:
        abort(400, description="Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    name = data.get('name')
    if name is None:
        abort(400, description="Missing name")

    new_place = Place(city_id=city_id, user_id=user_id, name=name)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@place_view.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200
