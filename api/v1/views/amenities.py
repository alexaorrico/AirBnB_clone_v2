#!/usr/bin/python3
"""Amenities module"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """Gets amenity objects"""
    amenities_list = []
    for i in storage.all(Amenity).values():
        amenities_list.append(i.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity_id(amenity_id):
    """Gets a certain amenity"""
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    else:
        return (jsonify(storage.get(Amenity, amenity_id).to_dict()))


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes an amenity based on id"""
    all_the_amenities = storage.get(Amenity, amenity_id)
    if all_the_amenities is None:
        abort(404)
    else:
        storage.delete(all_the_amenities)
        storage.save()
        return (jsonify({})), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """Creates a new amenity object"""
    data = request.get_json()
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    if "name" not in data:
        return (jsonify({"error": "Missing name"})), 400
    new_amenity_obj = Amenity(**data)
    new_amenity_obj.save()
    return (new_amenity_obj.to_dict()), 201


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["PUT"],
    strict_slashes=False)
def update_amenity(amenity_id):
    """Updates the amenity object"""
    data = request.get_json()
    all_the_amenities = storage.get(Amenity, amenity_id)
    if all_the_amenities is None:
        abort(404)
    if not data:
        return (jsonify({"error": "Not a JSON"})), 400
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(all_the_amenities, key, value)
    storage.save()
    return (jsonify(all_the_amenities.to_dict())), 200
