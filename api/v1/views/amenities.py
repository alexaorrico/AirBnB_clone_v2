#!/usr/bin/python3
""" Amenity Module"""


from models.amenity import Amenity
from models import storage
from flask import Flask, abort, jsonify, request, json
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """    Retrieves the list of all Amenity objects
    """
    amenities = []
    for key, value in storage.all("Amenity").items():
        amenities.append(value.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object by id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Create a new Amenity instance
    """
    if request.is_json:
        dicc = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' in dicc:
        new_amenity = Amenity()
        new_amenity.name = dicc["name"]
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        return jsonify({"error": "Missing name"}), 400


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update a Amenity instance
    """
    if not request.json:
        abort(400, "Not a JSON")
    amenity = storage.get("Amenity", id=amenity_id)
    if amenity:
        amenity.name = request.json['name']
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete a Amenity instance
    """
    amenity = storage.get("Amenity", id=amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)
