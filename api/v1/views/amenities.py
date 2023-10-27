#!/usr/bin/python3
"""amenities.py"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/amenities")
def get_amenities():
    """Retrieves the list of all """
    amenities = storage.all("Amenity").values()
    if amenities is None:
        abort(404)
    amenity_list = []
    for amenity in amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/api/v1/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/api/v1/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return ({}, 200)


@app_views.route("/api/v1/amenities", methods=['POST'])
def post_amenity():
    """Creates a Amenity"""
    data = request.get_json()
    if not data:
        return jsonify(404, "Not a JSON")
    if "name" not in data:
        return abort(404, "Missing name")
    amenity = Amenity(name=data['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/api/v1/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}, 400)
    to_be_ignored = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in to_be_ignored:
            setattr(Amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict(), 200)
