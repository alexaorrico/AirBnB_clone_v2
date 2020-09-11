#!/usr/bin/python3
""" Amenities view """
from models.amenity import Amenity
from api.v1.views import *
from flask import Flask, jsonify
from models import storage


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id=None):
    """GET Request for amenity"""
    if amenity_id:
        return get_model(Amenity, amenity_id)

    return jsonify([obj.to_dict() for obj in storage.all("Amenity").values()])


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """DELETE Request for amenity"""
    return delete(Amenity, amenity_id)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    """
        POST Request for an amenity
    """
    return post(Amenity, None, None, {"name"})


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """
        PUT Request for States
    """
    return put(Amenity, amenity_id, ["id", "created_at", "updated_at"])
