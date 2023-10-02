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

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """Creates amenities"""
    data = request.get_json()
    if not data:
        result = {"error": "Not a JSON"}
        return jsonify(result), 400

    name = data.get("name", None)
    if not name:
        result = {"error": "Missing name"}
        return jsonify(result), 400

    for amenity in storage.all("Amenity").values():
        if amenity.name == name:
            setattr(amenity, "name", name)
            amenity.save()
            result = amenity.to_dict()
            return jsonify(result), 200

    amenity = Amenity(**data)
    amenity.save()
    result = amenity.to_dict()
    return jsonify(result), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates amenity based on id"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        result = {"Error": "Not a JSON"}
        return jsonify(result), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    result = amenity.to_dict()
    return jsonify(result), 200
