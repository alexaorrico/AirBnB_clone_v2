#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves, Deletes or Updates a Place object by it's id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        return jsonify(place.to_dict())

    elif request.method == "DELETE":
        place.delete()
        storage.save()
        return jsonify({}), 200

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    nope = {"id", "user_id", "city_id", "created_at", "updated_at"}
    [setattr(place, key, val) for key, val in data.items() if key not in nope]
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    if "user_id" not in data:
        return "Missing user_id", 400
    user = storage.get("User", data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        return "Missing name", 400
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    nope = {"id", "user_id", "city_id", "created_at", "updated_at"}
    [setattr(place, key, val) for key, val in data.items() if key not in nope]
    place.save()
    return jsonify(place.to_dict()), 200
