#!/usr/bin/python3
"""
Places-Amenities view module: This module handles the API endpoints related to the interaction between Places and Amenities.
"""
from flask import abort, jsonify
from models import storage, Place, Amenity
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieve the list of all amenities associated with a specific Place.

    Args:
        place_id (str): The ID of the Place for which amenities are being retrieved.

    Returns:
        JSON: A JSON representation of the list of amenities associated with the Place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a specific Amenity object from a Place.

    Args:
        place_id (str): The ID of the Place from which the Amenity will be deleted.
        amenity_id (str): The ID of the Amenity to be deleted.

    Returns:
        JSON: An empty JSON response with a 200 status code upon successful deletion.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links a specific Amenity object to a Place.

    If the Amenity is already linked to the Place, it returns the existing link.

    Args:
        place_id (str): The ID of the Place to which the Amenity will be linked.
        amenity_id (str): The ID of the Amenity to be linked.

    Returns:
        JSON: A JSON representation of the linked Amenity with a 201 status code upon successful linking.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201
