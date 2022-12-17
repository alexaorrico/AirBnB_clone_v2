#!/usr/bin/python3
"""Module for Amenity endpoints"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'],
                 defaults={"amenity_id": None})
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities(amenity_id):
    """Retrieves the list of all Amenity objects
    or a specific amenity"""
    if amenity_id is None:
        return jsonify([v.to_dict() for v in storage.all(Amenity).values()])
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenities(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    """POST /amenity API route"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    s = Amenity(**data)
    s.save()
    return make_response(jsonify(s.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """PUT /amenity API route"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
