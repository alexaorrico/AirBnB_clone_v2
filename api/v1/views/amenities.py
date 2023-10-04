#!/usr/bin/python3
"""The `amenities` module"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def list_all_amenities():
    """Lists all amenities"""
    amenity = storage.all(Amenity)
    return jsonify([amenities.to_dict() for amenities in amenity.values()])


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def list_amenity_id(amenity_id):
    """Lists amenities by id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 404)


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes amenity by id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "name" not in payload:
        abort(400, "Missing name")
    new_amenity = Amenity(**payload)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity_id(amenity_id):
    """Updates amenity by id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    for key, value in payload.items():
        if key not in {"id", "created_at", "updated_at"}:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
