#!/usr/bin/python3
"""
    This Module contains all the api for the places
    Base route: /api/v1/places
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User

from flask import jsonify, request, abort


@app_views.route('cities/<city_id>/places', strict_slashes=True, methods=["GET"])
def get_cities_places(city_id=None):
    """This Method returns the places with a specific city_id"""
    if not city_id:
        abort(404)
    places = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    if not places:
        abort(404)
    return jsonify(places), 200


@app_views.route('/places/<place_id>', strict_slashes=True, methods=['GET'])
def get_places(place_id=None):
    """This Method returns the places with a place_id"""
    if not place_id:
        abort(404)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', strict_slashes=True, methods=['DELETE'])
def delete_place(place_id=None):
    """This method deletes a place based on the place_id"""
    if not place_id:
        None
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places/', strict_slashes=True, methods=['POST'])
def post_place(city_id=None):
    """This Method Creates a new Place"""
    if not city:
        abort(404)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.content_type != "application/json":
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "user_id" not in data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data.keys():
        return jsonify({"error": "Missing name"})
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=True, methods=['PUT'])
def put_place(place_id=None):
    """This Method updates the data of a currently existing place"""
    if not place_id:
        abort(404)
    if request.content_type != "application/json":
        return jsonify({"error": "Not a JSON"}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
    

