#!/usr/bin/python3
"""Amenities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import amenity
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities",
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects: GET /api/v1/amenities"""
    list = []
    amenity_obj = storage.all(Amenity).values()
    for a in amenity_obj:
        list.append(a.to_dict())
    return jsonify(list)


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities",
                 methods=['POST'],
                 strict_slashes=False)
def create_amenities():
    """Creates a Amenity: POST /api/v1/amenities"""
    obj_request = request.get_json()
    if obj_request:
        if 'name' in obj_request.keys():
            new_amenity_obj = Amenity(**obj_request)
            storage.new(new_amenity_obj)
            storage.save()
            current_state = storage.get(Amenity, new_amenity_obj.id)
            return jsonify(current_state.to_dict()), 201
        else:
            return "Missing name", 400
    else:
        return "Not a JSON", 400


@app_views.route("/amenities/<amenity_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def updates_amenities(amenity_id):
    """Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    amenity_obj = storage.get(Amenity, amenity_id)
    obj_request = request.get_json()
    if amenity_obj:
        if obj_request:
            for key, value in obj_request.items():
                ignore = ["id", "created_at", "updated_at"]
                if key not in ignore:
                    setattr(amenity_obj, key, value)
            storage.save()
            return (jsonify(amenity_obj.to_dict()), 200)
        else:
            return "Not a JSON", 400
    else:
        abort(404)
