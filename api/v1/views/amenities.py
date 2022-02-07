#!/usr/bin/python3
"""Amenities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities",
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects: GET /api/v1/amenities"""
    amenity_obj = storage.all(Amenity)
    for a in amenity_obj.values():
        return jsonify(a.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenities_id=None):
    """Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>"""
    amenity_obj = storage.get(Amenity, amenities_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities(amenity_id=None):
    """Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def create_amenities():
    """Creates a Amenity: POST /api/v1/amenities"""
    obj_request = request.get_json()
    if obj_request:
        if 'name' in obj_request:
            new_amenity_obj = Amenity(**obj_request)
            new_amenity_obj.save()
            return (jsonify(new_amenity_obj.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>",
                 methods=['PUT'], strict_slashes=False)
def updates_amenities(amenity_id):
    """Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    amenity_obj = storage.get(Amenity, amenity_id)
    obj_request = request.get_json()
    if amenity_obj:
        if obj_request:
            for key, value in obj_request.items():
                ignore = ["id", "created_at", "updated_at"]
                if key != ignore:
                    setattr(amenity_obj, key, value)
            amenity_obj.save()
            return (jsonify(amenity_obj.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
