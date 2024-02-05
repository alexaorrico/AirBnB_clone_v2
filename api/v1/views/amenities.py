#!/usr/bin/python3
"""a module as amenities API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    """a function to retrieve all amenities"""
    amenities = []
    all_amenities = storage.all("Amenity").values()
    for ament in all_amenities:
        amenities.append(ament.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """a function to get an amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """a function to delete an Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """a function to create a new Amenity object"""
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in json_req:
        return jsonify({"error": "Missing name"}), 400

    amenity = Amenity(name=json_req["name"])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """a function to update an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    try:
        json_req = request.get_json()
    except Exception:
        json_req = None

    if not json_req:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in json_req.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
