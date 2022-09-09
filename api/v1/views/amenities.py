#!/usr/bin/python3
"""
Amenity instance
"""

from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    """
    Retrieves the list of all Amenity objects
    """

    amenities = []

    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Retrieves the list of all State objects
    """

    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity instance"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    else:
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST "], strict_slashes=False)
def create_amenity():
    """Creates a City instance"""
    body = request.get_json()

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in body.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)

    amenity = Amenity(**body)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a City instance"""

    body = request.get_json()
    no_update = ["id", "created_at", "updated_at"]

    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)
    else:
        for key, value in body.items():
            if key not in no_update:
                setattr(amenity, key, value)
            else:
                pass

        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
