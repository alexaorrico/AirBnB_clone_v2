#!/usr/bin/python3
"""
Module to create view for Amenity objects handling default
RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/", methods=["GET"])
def amenities_get():
    """
    Retrieves list of all Amenity objects.
    """
    all_amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in all_amenities.values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<string:amenity_id>", methods=["GET"])
def amenity_id_get(amenity_id):
    """
    Retrieves an amenity with a given id
    Raise 404 error if id not linked to any Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"])
def amenity_id_delete(amenity_id):
    """
    Deletes an Amenity object with a given id
    Raise 404 error if id not linked to any Amenity object
    Returns and empty dictionary with status code 200
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities/", methods=["POST"])
def amenity_post():
    """
    Creates an Amenity via POST
    If the HTTP body request is not valid JSON, raise 400 error, Not a JSON
    If the dictionary doesn't contain the key name, raise a 400 error with
    message Missing name
    Returns new Amenity with status code 201
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenity/<string:amenity_id>", methods=["PUT"])
def amenity_put(state_id):
    """
    Updates an Amenity object via PUT
    If the amenity_id is not linked to any Amenity object, raise 404 error
    If the HTTP body request is not valid JSON, raise a 400 error, Not a JSON
    Update the Amenity object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    """
    amenity = storage.get(Amenity, state_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
