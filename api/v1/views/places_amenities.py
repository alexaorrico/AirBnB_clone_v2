#!/usr/bin/python3
""" Module containing Amenity View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.amenity import Amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects associated with a Place
        object.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        If retrieving from db storage, a list of dictionaries representing
        Amenity objects in JSON format is returned.
        If retrieving from file storage, a list of amenity ids in JSON format
        is returned.
        404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if storage_t == 'db':
        amenities = [amenity.to_dict() for amenity in place_obj.amenities]
    else:
        amenities = place_obj.amenity_ids
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def unlink_amenity(place_id, amenity_id):
    """ Remove an Amenity object from a Place object.

    Args:
        place_id (str): The UUID4 string representing a Place object.
        amenity_id (str): The UUID4 string representing a Amenity object.

    Returns:
        Returns an empty dictionary with the status code 200.
        404 error if:
            `place_id` is not linked to any Place object.
            `amenity_id` is not linked to any Amenity object.
            The Amenity object associated with `amenity_id` is not linked to
            the Place object associated with `place_id`.
    """
    place_obj = storage.get("Place", place_id)
    amenity_obj = storage.get("Amenity", amenity_id)
    if None in [place_obj, amenity_obj]:
        abort(404)
    if storage_t == 'db':
        if amenity_obj not in place_obj.amenities:
            abort(404)
    else:
        if amenity_obj.id not in place_obj.amenity_ids:
            abort(404)
    if storage_t == 'db':
        place_obj.amenities.remove(amenity_obj)
    else:
        place_obj.amenity_ids.remove(amenity_obj.id)

    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ Links an Amenity object to a Place object.

    Args:
        place_id (str): The UUID4 string representing an existing Place object.
        amenity_id (str): The UUID4 stirng representing an existing Amenity
        object.

    Returns:
        Returns the Amenity object as a  dictionary in JSON format with the
        status code 201.
        404 error if:
            `place_id` is not linked to any Place object.
            `amenity_id` is not linked to any Amenity object.
        200 status if the Amenity object associated with `amenity_id` is
        already linked to the Place object associated with `place_id`.
    """
    place_obj = storage.get("Place", place_id)
    amenity_obj = storage.get("Amenity", amenity_id)
    if None in [place_obj, amenity_obj]:
        abort(404)
    if storage_t == 'db':
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict())
    else:
        if amenity_obj.id in place_obj.amenity_ids:
            return jsonify(amenity_obj.to_dict())
    if storage_t == 'db':
        place_obj.amenities.append(amenity_obj)
    else:
        place_obj.amenity_ids.append(amenity_obj.id)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 201
