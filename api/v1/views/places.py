#!/usr/bin/python3


from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def fetch_places():
    """Fetch all places from the store"""
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_place_by_id(place_id: int):
    """Fetch a single place by it's ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id: int):
    """Delete an place by it's ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id: int):
    """Create a new place"""
    city = storage.get(City, id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_id = request.json['user_id']
    if not user_id:
        abort(400, description='Missing user_id')

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    content = request.get_json()
    place = Place(**content)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update an place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']

    content = request.get_json()
    for key, value in content.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
