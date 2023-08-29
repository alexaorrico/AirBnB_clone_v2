#!/usr/bin/python3
"""Place views for API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Return places list in format JSON"""
    places = storage.all(Place)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    lis_place = []
    for place in places.values():
        if city.id == place.city_id:
            lis_place.append(place.to_dict())
    return jsonify(lis_place)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Return a specific places object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete place id"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if "user_id" not in data:
        abort(400, 'Missing user_id')
    if "name" not in data:
        abort(400, 'Missing name')

    if not storage.get(City, city_id):
        abort(404)
    if not storage.get(User, data["user_id"]):
        abort(404)

    new_place = Place(**data)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update given place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
