#!/usr/bin/python3
"""
    This module creates a new view for Amenity
    objects that handles all default REST API
    actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves all amenities in storage"""
    all_amenities = storage.all(Amenity).values()
    amenity_list = []
    for amenity in all_amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_specific_amenity(amenity_id):
    """Return the amenity with given id"""
    search_result = storage.get(Amenity, amenity_id)
    if search_result:
        return jsonify(search_result.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_specific_amenity(amenity_id):
    """Delete the amenity with given id"""
    search_result = storage.get(Amenity, amenity_id)
    if search_result:
        storage.delete(search_result)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities/", methods=['POST'],
                 strict_slashes=False)
def post_new_amenity():
    """Post a new state to the db"""
    try:
        amenity_dict = request.get_json()

    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if amenity_dict.get("name"):
        new_amenity = Amenity(**amenity_dict)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201

    return jsonify({"error": "Missing name"}), 400


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def modify_amenity(amenity_id):
    """Modify an existing amenity in the db"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        try:
            update_dict = request.get_json()
            for key in ('id', 'created_at', 'updated_at'):
                if update_dict.get(key):
                    del update_dict[key]

        except Exception:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in update_dict.items():
            setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200

    else:
        abort(404)
