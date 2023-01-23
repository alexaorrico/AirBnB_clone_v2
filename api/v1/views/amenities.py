#!/usr/bin/python3
"""Amenities API"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False,
                 methods=['GET'])
@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """Retrieves the list of all Amenity objects or Amenity object"""

    if amenity_id is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    amenities = list(storage.all(Amenity).values())
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete a Amenity"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False,
                 methods=['POST'])
def create_amenity():
    """Create an Amenity"""

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    name = data.get("name", None)
    if name is None:
        abort(400, description="Missing name")
    amenity = Amenity(name=name)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    data = {k: v for k, v in data.items() if k != 'id' and
            k != 'created_at' and k != 'updated_at'}
    for k, v in data.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
