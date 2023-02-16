#!/usr/bin/python3

"""amenities view module"""

from api.v1.views import (app_views)
from models.amenity import Amenity
from flask import jsonify, abort, request
import models


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def amenities():
    """return all the amenities"""
    all_amenities = models.storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in all_amenities.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=["GET"], strict_slashes=False)
def get_amenities_by_id(amenity_id):
    """return a amenity by id or 404"""
    amenity = models.storage.get(Amenity, amenity_id)
    if amenity_id is None:
        return abort(404)
    if amenity is None:
        return abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity data by id"""
    amenity = models.storage.get(Amenity, amenity_id)
    if amenity_id is None:
        return abort(404)
    if amenity is None:
        return abort(404)
    else:
        models.storage.delete(amenity)
        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def add_amenity():
    """add new amenity"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        req_data = None

    if req_data is None:
        return "Not a JSON", 400

    if "name" not in req_data.keys():
        return "Missing name", 400

    new_amenity = Amenity(**req_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity object"""
    try:
        req_data = request.get_json(force=True)
    except Exception:
        return "Not a JSON", 400
    amenity = models.storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    for key in ("id", "created_at", "updated_at"):
        req_data.pop(key, None)
    for k, v in req_data.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
