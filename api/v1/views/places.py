#!/usr/bin/python3
"""file places"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort
import json

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id=None):
    """Functon places"""
    list_of_places = []
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    for place in cities.places:
        list_of_places.append(place.to_dict())
    return jsonify(list_of_places)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def placesid(place_id=None):
    """Places id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def placesdel(place_id=None):
    """Places id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postplaces(city_id=None):
    """Post places"""
    body = request.get_json()
    if body is None:
        return jsonify({
            "error": "Not a JSON"
        }), 400
    elif 'user_id' not in body.keys():
        return jsonify({
            "error": "Missing user_id"
        }), 400
    elif 'name' not in body.keys():
        return jsonify({
            "error": "Missing name"
        }), 400

    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    user_id = body.get("user_id")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    new_place = Place(**body)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def putplaces(place_id=None):
    """Put places"""
    notAttr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    body = request.get_json()
    if body is None:
        return jsonify({
            "error": "Not a JSON"
        }), 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for key, value in body.items():
        if key not in notAttr:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
