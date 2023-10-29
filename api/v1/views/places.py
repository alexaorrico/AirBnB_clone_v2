#!/usr/bin/python3
"""Create a new view for Place objects"""
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place Object"""
    place = storage.get(Place, Place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    new = Place(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_key:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
