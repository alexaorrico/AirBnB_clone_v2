#!/usr/bin/python3
"""Module for City related endpoints"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage
from models.amenity import Amenity

model = "Amenity"
parent_model = None


@app_views.route("/amenities", strict_slashes=False,
                 methods=["GET"], defaults={"amenity_id": None})
@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """GET /aminities api route"""
    if not amenity_id:
        list_objs = [v.to_dict() for v in storage.all(model).values()]
        return jsonify(list_objs)

    return get_model(model, amenity_id)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """DELETE /amenity api route"""
    return delete_model(model, amenity_id)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    """POST /amenity api route"""
    required_data = {"name"}
    return post_model(model, None, None, required_data)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """PUT /amenity api route"""
    ignore_data = ["id", "created_at", "updated_at"]
    return put_model(model, amenity_id, ignore_data)
