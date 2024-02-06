#!/usr/bin/python3
"""This module contains the view for the place amenties resource."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models import storage


@app_views.route(
        "/places/<place_id>/amenities",
        strict_slashes=False,
        methods=["GET"]
        )
@app_views.route(
        "/places/<place_id>/amenities/<amenity_id>",
        strict_slashes=False,
        methods=["GET", "DELETE", "POST"]
        )
def amenities_view(place_id, amenity_id=None):
    """ View functions to retrieve the amenities
    objects"""
    place_object = storage.get(Place, place_id)
    if place_object is None:
        abort(404)
    if request.method == "GET":
        return jsonify(
                [obj.to_dict() for obj in place_object.amenities]
                )
    if request.method == "DELETE":
        if not storage.get(Amenity, amenity_id):
            abort(404)
        amenity_ids = [
                amenity_obj.get("id", None)
                for amenity_obj in place_object.amenities
                ]
        if amenity_id not in amenity_ids:
            abort(404)
        #  Get amenity object and delete.
        storage.delete(storage.get(Amenity, amenity_id))
        storage.save()
        return jsonify({}}, 200
    if request.method == "POST":
        if not storage.get(Amenity, amenity_id):
            abort(404)
        amenity_ids = [
                amenity_obj.get("id", None)
                for amenity_obj in place_object.amenities
                ]
        if amenity_id in amenity_ids:
            return jsonify(storage.get(Amenity, amenity_id)), 200
        # link amenity to place...
        amenity_object = storage.get(Amenity, amenity_id)
        place_object.amenities.append(amenity_object)
        return jsonify(amenity_object.to_dict()), 201
