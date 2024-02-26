#!/usr/bin/python3
"""
Amenities view
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenity_list = [
        amenity.to_dict() for amenity in storage.all("Amenity").values()
        ]
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a specific Amenity object by ID"""
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a specific Amenity object by ID"""
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object"""
    amenity_data = request.get_json(silent=True)
    if amenity_data is None:
        abort(400, "Not a JSON")

    if "name" not in amenity_data:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity_data)
    new_amenity.save()

    resp = jsonify(new_amenity.to_dict())
    resp.status_code = 201
    return resp


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a specific Amenity object by ID"""
    amenity_data = request.get_json(silent=True)
    if amenity_data is None:
        abort(400, "Not a JSON")

    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)

    for key, value in amenity_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)

    amenity_obj.save()

    resp = jsonify(amenity_obj.to_dict())
    resp.status_code = 200
    return resp
