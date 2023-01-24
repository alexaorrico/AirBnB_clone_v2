#!/usr/bin/python3
"""Amenity view"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'],
                 strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """
    get amenities or get a particular amenity
    """
    new_list = []
    key = "Amenity." + str(amenity_id)
    if amenity_id is None:
        objs = storage.all(Amenity)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(Amenity).keys():
        return jsonify(storage.all(Amenity)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    delete amenity based on the amenity_id passed
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """
    create a new amenity
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """
    update amenity that the id was passed
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    key = "Amenity." + str(amenity_id)
    if key not in storage.all(Amenity).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    for key, value in request.get_json().items():
        if key not in ["created_at", "updated_at", "id"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
