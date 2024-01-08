#!/usr/bin/python3
"""
contains endpoints(routes) for place_amenities objects
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<string:place_id>/amenities", strict_slashes=False)
def get_amenities(place_id):
    """
    Retrieves the list of all amenities objects of a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def del_amenity(place_id, amenity_id):
    """
    Deletes a amenity object from place
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 strict_slashes=False, methods=['POST'])
def post_amenity2(place_id, amenity_id):
    """ post amenity by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return (jsonify(amenity.to_dict()), 200)
    place.amenities.append(obj)
    storage.save()
    return (jsonify(amenity.to_dict(), 201))
