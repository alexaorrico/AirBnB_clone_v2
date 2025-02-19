#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
import os
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from flask import abort, request, jsonify

# Depending of the storage:

db_mode = os.getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def place_amenities(place_id):
    """retrieve place amenities"""
    amenities_list = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if db_mode == "db":
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    for amenity in amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity_from_place(place_id, amenity_id):
    """delete an amenity my id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if db_mode == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id

    for amenity in place_amenities:
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route("places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["POST"])
def link_amenity(place_id, amenity_id):
    """Link Amenity to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if db_mode == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id

    if amenity not in place_amenities:
        place_amenities.append(amenity)
        storage.save()
    else:
        return jsonify(amenity.to_dict()), 200

    return jsonify(amenity.to_dict()), 201
