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


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenis(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    list_ameniti = []
    for i in place.amenities:
        list_ameniti.append(i.to_dict())
    return jsonify(list_ameniti)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place_amenity(place_id, amenity_id):
    """Delete amenity by place and amenity id"""
    place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if the_amenity is None:
        abort(404)
    storage.delete(the_amenity)
    storage.save()
    return jsonify({}), 200

# @app_views.route('places/<place_id>/amenities/<amenity_id>',
#                  methods=['DELETE'],
#                  strict_slashes=False)
# def amenis_delete(place_id, amenity_id):
#     places = storage.get("Place", place_id)
#     if place is None:
#         abort(404)
#     amenits = storage.get("Amenity", amenity_id)
#     if amenits is None:
#         abort(404)
#     for key, value in places.amenties.items():
#         if value.id == amenity_id:
#             storage.delete(amenits)
#             storage.save()
#             return jsonify({}), 200
#     abort(404)
