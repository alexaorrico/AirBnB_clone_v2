#!/usr/bin/python3
""" Flask routes for handling URI subpaths concerning `Place` - `Amenity`
object relationships in storage, using `app_views` Blueprint.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def GET_Place_amenities(place_id):
    """ Returns JSON list of all `Amenity` instances associated
    with a given `Place` instance in storage

    Args:
        place_id: uuid of `Place` instance in storage

    Return:
        JSON list of all `Amenity` instances for a given `Place` instance
    """
    place = storage.get(Place, place_id)

    if place:
        amenity_list = []
        for amenity in place.amenities:
            amenity_list.append(amenity.to_dict())
        return (jsonify(amenity_list))
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def DELETE_Place_amenities(place_id, amenity_id):
    """ Deletes relationship between a `Place` and an `Amenity` instance in
    storage by ids in URI subpath

    Args:
        place_id: uuid of `Place` instance in storage
        amenity_id: uuid of `Amenity` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place and amenity and amenity in place.amenities:
        place.amenities.remove(amenity)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def POST_Place_amenities(place_id, amenity_id):
    """ Links a new `Amenity` instance to a `Place` instance in storage,
    by ids in URI subpath

    Args:
        place_id: uuid of `Place` instance in storage
        amenity_id: uuid of `Amenity` instance in storage

    Return:
        Linked `Amenity` instance and response status 201, or 404 response
    on error
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place and amenity:
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()))
        else:
            place.amenities.append(amenity)
        storage.save()
        return (jsonify(amenity.to_dict()), 201)
    else:
        abort(404)
