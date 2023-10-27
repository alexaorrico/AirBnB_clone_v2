#!/usr/bin/python3
"""
API endpoints related to linking Place objects and Amenity objects.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieve a list of all amenities associated with a Place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON response containing a list of amenity data.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Delete an Amenity from a Place.

    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity to delete.

    Returns:
        Empty JSON response with a status code.
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Link an Amenity to a Place.

    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity to link.

    Returns:
        JSON response containing the linked Amenity with a status code.
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
