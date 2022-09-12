#!/usr/bin/python3
"""file places_reviews"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
import json
from os import getenv

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}

storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def place_amenities(place_id):
    """Get the amenities by place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_a = []
    for i in place.amenities:
        list_a.append(i.to_dict())
    return jsonify(list_a)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amenity(place_id, amenity_id):
    """Delete amenity by place and amenity id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def add_amenity(place_id, amenity_id):
    """POST a new amenity on a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
