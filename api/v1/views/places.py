#!/usr/bin/python3
"""places endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """get places"""
    city = storage.get(City, city_id)
    print
    if city is None:
        abort(404)
    places = []
    places_db = storage.all(Place).values()
    for place in places_db:
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places), 200


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """get a specific place"""
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a specific place"""
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """create a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """modify a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
