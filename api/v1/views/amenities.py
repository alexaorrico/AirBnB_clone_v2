#!/usr/bin/python3
"""module for amenities view"""
from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False, methods=["GET"])
def get_amenites(amenity_id=None):
    """retrives all amenities"""
    if (not amenity_id):
        amenities = storage.all(Amenity)
        result = []
        for a in amenities.values():
            result.append(a.to_dict())
        return jsonify(result)
    else:
        required_amenity = storage.get(Amenity, amenity_id)
        if (not required_amenity):
            abort(404)
        return jsonify(required_amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False, methods=["DELETE"])
def delete_amenity(amenity_id):
    """deletes an amenity instance"""
    required_amenity = storage.get(Amenity, amenity_id)
    if (not required_amenity):
            abort(404)
    storage.delete(required_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """creates an amenity"""
    if not request.json:
        return make_response("Not a JSON", 400)
    if not 'name' in request.json:
        return make_response("Missing name", 400)

    new_amenity = Amenity(**(request.get_json()))
    new_amenity.save()
    return new_amenity.to_dict(), 201


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False, methods=["PUT"])
def edit_amenity(amenity_id):
    """edits an amenity"""
    required_amenity = storage.get(Amenity, amenity_id)
    if (not required_amenity):
        abort(404)
    if not request.json:
        return make_response("Not a JSON", 400)

    input_dict = request.get_json()
    for key, value in input_dict.items():
        if (key not in ["id", "created_at", "updated_at"]):
            if (hasattr(required_amenity, key)):
                setattr(required_amenity, key, value)
    required_amenity.save()
    return required_amenity.to_dict(), 200
