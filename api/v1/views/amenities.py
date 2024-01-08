#!/usr/bin/python3
"""Amenity view"""


from models.amenity import Amenity
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage


@app_views.route('/amenities', methods=["GET", "POST"])
def amenities():
    """retrieve or create amenities depending on request method"""
    if request.method == "GET":
        amenity = storage.all(Amenity).values()
        amenity_list = []
        for a in amenity:
            amenity_list.append(a.to_dict())
        amenity_list_json = jsonify(amenity_list)
        return amenity_list_json
    else:
        amenity_dict = request.get_json()
        if amenity_dict is None:
            abort(400, "Not a JSON")
        if "name" not in amenity_dict:
            abort(400, "Missing name")
        new_amenity = Amenity({"name": amenity_dict.get("name")})
        new_amenity.save()
        new_amenity_json = jsonify(new_amenity.to_dict())
        return new_amenity_json


@app_views.route('/amenities/<amenity_id>', methods=["GET"])
def amenities_id(amenity_id):
    """retrieve amenity with id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_json = jsonify(amenity.to_dict())
    return amenity_json


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_amenity(amenity_id):
    """delete an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_dict = request.get_json()
    if amenity_dict is None:
        abort(400, "Not a JSON")

    # easier way to update objects
    # AND update all object attributes
    # not just the name

    for k, v in amenity_dict.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    amenity_json = jsonify(amenity.to_dict())
    return amenity_json
