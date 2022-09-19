#!/usr/bin/python3
"""Module amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import *


@app_views.route('/amenities', methods=['GET'], strict_slashes=False,
                 defaults={'state_id': None})
@app_views.route('/amenities/<amenity_id>/', methods=['GET'], strict_slashes=False,)
def get_amenity(amenity_id):
    """Retrieves amenity object"""
    if amenity_id is None:
        list_amenities = []
        for amenity in storage.all('Amenity').values():
            list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)
    save = storage.get(Amenity, amenity_id)
    if not save:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(save.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id=None):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    """Creates a Amenity"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    s = Amenity(**data)
    s.save()
    return make_response(jsonify(s.to_dict()), 201)


@app_views.route("/amenities", strict_slashes=False, methods=["PUT"])
def put_amenity(amenity_id=None):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ["id", "created_at", "updated_at"]
    if not amenity:
        return make_response(jsonify({"error": "Not found"}), 404)
    else:
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
