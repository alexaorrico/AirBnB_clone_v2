#!/usr/bin/python3
"""handles all defaults RESTful API actions for place and amenity"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities_place(place_id):
    """retrieves the list of all amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """deletes amenity of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity_place(place_id, amenity_id):
    """creates a new amenity of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
