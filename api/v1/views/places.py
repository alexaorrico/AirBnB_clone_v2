#!/usr/bin/python3
"""Place API"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """get method for places in a  city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    city_place = []
    for place in places.values():
        if place.city_id == city_id:
            city_place.append(place.to_dict())
    return jsonify(city_place)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Get a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a Place"""
    if storage.get(City, city_id) is None:
        abort(404)
    get_json = request.get_json()
    if get_json is None:
        abort(400, 'Not a JSON')
    if get_json.get('name') is None:
        abort(400, 'Missing Name')
    if get_json.get('user_id') is None:
        abort(400, 'Missing user_id')
    user_id = get_json.get('user_id')
    if (storage.get(User, user_id) is None):
        abort(404)

    get_json['city_id'] = city_id
    new_place = Place(**get_json)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    update = request.get_json()

    exept = ['created_at', 'updated_at', 'id', 'user_id', 'city_id']
    for key, value in update.items():
        if key not in exept:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
