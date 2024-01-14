#!/usr/bin/python3
"""Handles all RESTful API actions for `Amenity`"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

from flask import jsonify, abort, request


@app_views.route("/amenities")
def amenities():
    """Retrieve list of all `Amenity` objects

    Returns:
        `flask.Response`: List of all the amenities
    """
    amenities = storage.all(Amenity)
    result = []

    for amenity in amenities.values():
        result.append(amenity.to_dict())

    return jsonify(result)


@app_views.route("/amenities/<amenity_id>")
def amenity(amenity_id):
    """Retrieve one `Amenity`

    Args:
        amenity_id (str): Amenity identifier

    Returns:
        flask.Response: An amenity in json
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete an amenity.

    Args:
        amenity_id (str): The ID of the amenity.

    Returns:
        dict: An empty JSON.

    Raises:
        404: If the specified amenity_id does not exist.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Create an amenity

    Returns:
        dict: New amenity in JSON

    Raises:
        400: If request body is not a valid JSON
        400: If the payload does not contain the key `name`
    """
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "name" not in payload:
        abort(400, "Missing name")

    amenity = Amenity(**payload)
    amenity.save()

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    payload = request.get_json()
    if not amenity:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")

    key = "name"
    setattr(amenity, key, payload[key])
    amenity.save()

    return jsonify(amenity.to_dict())
