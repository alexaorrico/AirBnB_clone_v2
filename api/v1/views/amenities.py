#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from flasgger.utils import swag_from
from flask import Flask, abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
@swag_from("documentation/amenity/get.yml", methods=["GET"])
def get_all_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["GET"], strict_slashes=False
)
@swag_from("documentation/amenity/get_id.yml", methods=["GET"])
def get_amenity_id(amenity_id):
    """Retrieves a specific amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["DELETE"], strict_slashes=False
)
@swag_from("documentation/amenity/delete.yml", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes a  amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
@swag_from("documentation/amenity/post_amenity.yml", methods=["POST"])
def post_amenity():
    """
    Creates a amenity
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    body = request.get_json()
    instance = Amenity(**body)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["PUT"], strict_slashes=False
)
@swag_from("documentation/amenity/put.yml", methods=["PUT"])
def put_amenity(amenity_id):
    """PUTs a  amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in dict(request.get_json()).items():
        setattr(amenity, key, val)

    storage.save()

    return jsonify(amenity.to_dict())
