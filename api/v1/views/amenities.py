#!/usr/bin/python3
"""
    Module of blueprints of flask
"""
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def fetch_all_amenities():
    """Fetch all amenities"""
    amenities_list = []
    amenities = storage.all("Amenity")
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def fetch_amenity(amenity_id):
    """Fetch a amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenity"""
    post_data = request.get_json()
    if post_data is None:
        abort(400, 'Not a JSON')
    if post_data.get('name') is None:
        abort(400, 'Missing name')
    new_amenity = Amenity(**post_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity"""
    attributes_unchanged = ['id', 'created_at', 'updated_at']
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    put_data = request.get_json()
    if put_data is None:
        abort(400, 'Not a JSON')
    for key, value in put_data.items():
        if key in attributes_unchanged:
            pass
        else:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
