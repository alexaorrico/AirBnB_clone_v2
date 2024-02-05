#!/usr/bin/python3
"""module to handle amenity API request"""
from models.amenity import Amenity
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """method to get all amenities"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """method to get amenity by id"""
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """method to delete amenity by id"""
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            amenity.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """method to create a new amenity"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    if 'name' not in request_data.keys():
        abort(400, "Missing name")
    new_amenity = Amenity(**request_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """method to update amenity"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            for attrib, value in request_data.items():
                if attrib in ["id", "created_at", "updated_at"]:
                    continue
                setattr(amenity, attrib, value)
            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 200)
    abort(404)
