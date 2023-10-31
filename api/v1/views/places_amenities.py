#!/usr/bin/python3
"""
API endpoints related to linking Place objects and Amenity objects.
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<string:place_id>/amenities", methods=["GET"],
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
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
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
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=["POST"], strict_slashes=False)
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
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
