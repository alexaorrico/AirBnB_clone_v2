#!/usr/bin/python3
"""
Amenity api
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_all():
    """get all amenities"""
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """get a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """post a new amenity"""
    amenity = request.get_json()
    if amenity is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in amenity:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**amenity)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """update a specific amenity"""
    data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            print(key, value)
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
