#!/usr/bin/python3
"""Place-Amenity hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from os import getenv


@app_views.route(
    "/places/<string:place_id>/amenities",
    methods=["POST"],
    strict_slashes=False,
)
def get_place_amenities(place_id):
    """Get Amenity info of specified place."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity)
    return jsonify(amenities)


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def delete_place_amenity(place_id, amenity_id):
    """Delete an aminity of the specified place."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def add_amenity_to_place(place_id, amenity_id):
    """Add an Amenity to the specified place."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
