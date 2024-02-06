#!/usr/bin/python3
"""Handles all RESTful API actions for the `place_amenity` relationship"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t as storage_type


@app_views.route("/places/<place_id>/amenities")
def amenities_of_a_place(place_id):
    """Retrieve all amenities of a place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = place.amenities if storage_type == "db" else place.amenity_ids
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"])
def unlink_amenity_from_a_place(place_id, amenity_id):
    """Unlink amenity from a place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity or amenity not in place.amenities:
        abort(404)

    if storage_type == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity)

    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_amenity_to_a_place(place_id, amenity_id):
    """Link amenity to a place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict())

    if storage_type == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
