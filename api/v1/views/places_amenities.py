#!/usr/bin/python3
"""This is the api places_amenities module to link Place and Amenity"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, Amenity
"""These are the imported modules and or packages"""


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """Retrieves a list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes an Amenity object from a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
