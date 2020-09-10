#!/usr/bin/python3
"""
Amenity Api Module
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Return All Amenities
    """
    amenity_objs = storage.all('Amenity').values()
    amenities = [amenity.to_dict() for amenity in amenity_objs]
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities_ID(amenity_id):
    """
    Return Amenity by ID
    """
    try:
        return jsonify(storage.get("Amenity", amenity_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'])
def delete_amenity_id(amenity_id):
    """
    Deletes an Amenity by id
    """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    try:
        storage.delete(storage.get('Amenity', amenity_id))
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """
    Create Amenity
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    amenity_dict = request.get_json()
    if "name" not in amenity_dict:
        return jsonify({"error": "Missing name"}), 400
    else:
        amen_name = amenity_dict["name"]
        amenity = Amenity(name=amen_name)
        for key, value in amenity_dict.items():
            setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    Update Amenity by id
    """
    amenity = storage.get("Amenity", amenity_id)
    info_fields = ["id", "created_at", "updated_at"]
    if not amenity:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    response = request.get_json()
    for key, value in response.items():
        if key not in info_fields:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
