#!/usr/bin/python3
""" View for amenities objects """

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request

@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def amenities():
    """ method to get all amenities """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ method to get amenity id"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict()), 200

@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ method to delete amenity """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200

@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """ method to create a new amenity """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()

    return jsonify(amenity.to_dict()), 201

@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Method to update an amenity """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, val in data.items():
        if key in ["id", "created_at", "updated_at":
            continue
        setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
