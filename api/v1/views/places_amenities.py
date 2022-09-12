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
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<p_id>/amenities/<a_id>", strict_slashes=False,
                 methods=['POST'])
def post_place_amenity(p_id, a_id):
        """POST a new amenity on a place"""
        the_place = storage.get(Place, p_id)
        if the_place is not None:
            the_amenity = storage.get(Amenity, a_id)
            if the_amenity is not None:
                place_amenity = the_place.amenities
                if the_amenity in place_amenity:
                    return jsonify(the_amenity.to_dict(), 200)
                place_amenity.append(the_amenity)
            abort(404)
        abort(404)
