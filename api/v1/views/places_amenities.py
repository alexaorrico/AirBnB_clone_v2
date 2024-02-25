#!/usr/bin/python3
"""
Module docstring
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
from flasgger import swag_from


@app_views.route("/places/<string:place_id>/amenities",
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places_amenities/GET_ALL_places_amenities.yml')
def http_get_all_amenities_from_place_by_id(place_id):
    """
    Function http_get_all_amenities_from_place_by_id retrieves all amenities
    associated with a specific place.

    """


@app_views.route("/places/<string:place_id>/amenities",
                 methods=['GET'], strict_slashes=False)
def get_all_amenities_from_place_by_id(place_id):
    """
    Function get_all_amenities_from_place_by_id retrieves all amenities
    associated with a specific place.

    It takes an id parameter and returns the list of all amenities for this
    place.

    :param place_id: Retrieves the place object from the database
    :return: A list of all amenities
    :doc-author: Trelent
    """

    instance_place = storage.get(Place, place_id)
    if instance_place is None:
        abort(404)
    all_amenities = instance_place.amenities if getenv(
        "HBNB_TYPE_STORAGE") == "db" else instance_place.amenity_ids
    list_amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(list_amenities), 200


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/places_amenities/DELETE_places_amenities.yml')
def delete_amenity_linked_to_place_by_id(place_id, amenity_id):
    """
    Function delete_amenity_linked_to_place_by_id deletes an amenity from a
    place.

    Requires two arguments, the id of the place and the id of the amenity
    to delete. If either is not found, it returns a 404 error.

    :param place_id: Retrieves the place object from storage
    :param amenity_id: Retrieves the id of the amenity object
    :return: The response
    :doc-author: Trelent
    """
    instance_place = storage.get(Place, place_id)
    if instance_place is None:
        abort(404)
    instance_amenity = storage.get(Amenity, amenity_id)
    if instance_amenity is None:
        abort(404)

    all_amenities = instance_place.amenities if getenv(
        "HBNB_TYPE_STORAGE") == "db" else instance_place.amenity_ids

    if instance_amenity not in all_amenities:
        abort(404)
    all_amenities.remove(instance_amenity)
    instance_place.save()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places_amenities/POST_places_amenities.yml')
def http_link_amenity_to_place_by_id(place_id, amenity_id):
    """
    Function http_link_amenity_to_place_by_id links an amenity to a place by
    id.

    """


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place_by_id(place_id, amenity_id):
    """
    Function link_amenity_to_place_by_id links an amenity to a place by id.

    It takes two arguments, the place_id and the amenity_id. It returns a
    jsonified dictionary of the new linked amenity and a status code of 200
    upon success or 404 if not found.

    :param place_id: Identifies the place object to which the
    :param amenity_id: Specifies the id of the amenity object
    :return: The amenity that was linked to the place,
    and returns a status code of 201
    :doc-author: Trelent
    """

    instance_place = storage.get(Place, place_id)
    if instance_place is None:
        abort(404)
    instance_amenity = storage.get(Amenity, amenity_id)
    if instance_amenity is None:
        abort(404)
    all_amenities = instance_place.amenities if getenv(
        "HBNB_TYPE_STORAGE") == "db" else instance_place.amenity_ids

    if instance_amenity in all_amenities:
        return jsonify(instance_amenity.to_dict()), 200
    all_amenities.append(instance_amenity)
    instance_place.save()
    return jsonify(instance_amenity.to_dict()), 201
