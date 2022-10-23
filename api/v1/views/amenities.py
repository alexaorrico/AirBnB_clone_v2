#!/usr/bin/python3
"""routes for amenities"""
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def get_amenities( ):
    """ retrieves the list of all Amenity"""
    amenities = storage.all(Amenity)
    all_amenities = []
    for amenity in amenities.values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=["GET"])
def get_amenity(amenity_id):
    """Retrieve a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """delete a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """creates a Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for attr, val in data.items():
        if attr not in ["id", "created_at", "updated_at"]:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
