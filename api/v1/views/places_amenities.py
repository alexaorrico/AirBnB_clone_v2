#!/usr/bin/python3
"""Handles all RESTful API actions for `place_amenity` relationship"""
from flask import jsonify, abort

from api.v1.views import app_views
from models.place import Place
from models import storage
from models import storage_t as storage_type
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities")
def amenities_of_a_place(place_id):
    """Retrieve all amenities of a place.

    Args:
        place_id (str): ID of the place to retrieve its amenities.

    Returns:
        list: All amenities of the place in JSON.

    Raises:
        404: If the specified place_id does not exist.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    result = []

    if storage_type == "db":
        for amenity in place.amenities:
            result.append(amenity.to_dict())
    else:
        result = place.amenities

    return jsonify(result)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def unlink_amenity_from_a_place(place_id, amenity_id):
    """Unlink amenity from a place.

    Args:
        place_id (str): ID of the place.
        amenity_id (str): ID of the amenity.

    Returns:
        dict: An empty JSON.

    Raises:
        404: If the specified place_id or amenity_id does not exist or if the
             amenity is not linked to the place before the request.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    if storage_type == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_amenity_to_a_place(place_id, amenity_id):
    """Link amenity to a place.

    Args:
        place_id (str): ID of the place.
        amenity_id (str): ID of the amenity.

    Returns:
        dict: The amenity linked.

    Raises:
        404: If the specified place_id or amenity_id does not exist.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())

    if storage_type == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()

    return jsonify(amenity.to_dict()), 201
