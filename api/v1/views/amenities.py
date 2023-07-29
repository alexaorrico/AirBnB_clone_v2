#!/usr/bin/python3
"""
This module handles the view for Amenities objects that handles
all default RESTFul API actions
"""

from flask import jsonify, abort, request
from api.v1.views import amenity_views
from models import storage
from models.amenity import Amenity


@amenity_views.route("/", methods=["GET"])
def list_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities_objs = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities_objs.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@amenity_views.route("/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """Retrieves an Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@amenity_views.route("/<string:amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@amenity_views.route("/", methods=["POST"])
def create_amenity():
    """Creates a new Amenity and stores it"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    if 'name' not in amenity_data:
        abort(400, "Missing name")
    amenity = Amenity(**amenity_data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@amenity_views.route("/<string:amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Updates an Amenity given by amenity_id and stores it"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    if len(request.data) == 0:
        abort(400, "Not a JSON")
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    for key, value in amenity_data.items():
        keys_to_ignore = ["id", "created_at", "updated_at"]
        if key not in keys_to_ignore:
            setattr(amenity, key, value)
    amenity.save()
    storage.save()
    amenity = amenity.to_dict()
    return jsonify(amenity), 200
