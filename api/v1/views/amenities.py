#!/usr/bin/python3
"""Flask application for Amaneties class/entity"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def retrieves_all_amaneties():
    """Retrieves the list of all Amenity"""
    amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns an object by id"""
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def deletes_amenities(amenity_id):
    """Deletes an object by id"""
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenities():
    """Creates an object"""
    amenities_data = request.get_json()
    if not amenities_data:
        abort(400, "Not a JSON")
    elif "name" not in amenities_data:
        abort(400, "Missing name")
    new_amenities = Amenity(**amenities_data)
    new_amenities.save()
    return jsonify(new_amenities.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """Updates an object"""
    amenities_data = request.get_json()
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    if not amenities_data:
        abort(400, "Not a JSON")

    for key, value in amenities_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenities, key, value)
    storage.save()
    return jsonify({}), 200
