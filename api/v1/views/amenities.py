#!/usr/bin/python3
""" Creates API actions for amenities"""

from flask import Flask, abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenity():
    """Retrieves the list of all amenities"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves amenities based on id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    result = amenity.to_dict()
    return jsonify(result)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes amenity based on id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """Creates amenities"""
    amenity = request.get_json()
    if not amenity:
        abort(400, "Not a JSON")

    if "name" not in amenity:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity)
    storage.new(new_amenity)
    storage.save()

    result = amenity.to_dict()
    return make_response(jsonify(result), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates amenity based on id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    update = request.get_json()
    if not update:
        abort(400, "Not a JSON")

    keys_to_exclude = ["id", "created_at", "updated_at"]
    for key in keys_to_exclude:
        update.pop(key, None)

    for key, value in update.items():
        setattr(update, key, value)

    storage.save()
    result = amenity.to_dict()
    return make_response(jsonify(result), 200)
