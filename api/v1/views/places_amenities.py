#!/usr/bin/python3
"""
    Module of blueprints of flask
"""
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def fetch_all_places_amenities(place_id):
    """Fetch all amenitys"""
    amenities_list = []
    check_place = storage.get("Place", place_id)
    if check_place is None:
        abort(404)
    for amenities in check_place.amenities:
        amenities_list.append(amenities.to_dict())
    return jsonify(amenities_list), 200


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenities(place_id, amenity_id):
    """Delete a review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def create_place_amenities(place_id, amenity_id):
    """Creates an amenity"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
