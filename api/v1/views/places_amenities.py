#!/usr/bin/python3
"""Place-Amenity hanlders."""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from os import getenv
from models.place import Place
from models.amenity import Amenity


@app_views.route(
    "/places/<string:place_id>/amenities",
    methods=["GET"],
    strict_slashes=False,
)
def get_place_amenities(place_id):
    """Get Amenity info of specified place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>",
    methods=["DELETE"],
    strict_slashes=False,
)
def delete_place_amenity(place_id, amenity_id):
    """Delete an aminity of the specified place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)
    place.save()
    return jsonify({})


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>",
    methods=["POST"],
    strict_slashes=False,
)
def add_amenity_to_place(place_id, amenity_id):
    """Add an Amenity to the specified place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
