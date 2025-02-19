#!/usr/bin/python3
"""
Create a new view for Amenity objects
that handles all default RESTFul API actions
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    all_amenity = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in all_amenity]
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a State object"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a Amenity use POST request"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()

    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def updata_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)

    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
