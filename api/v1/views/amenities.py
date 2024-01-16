#!/usr/bin/python3
"""Creating an api for amenities"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenities_or_amenity(amenity_id=None):
    """ gets all amenity objects if id is none of one amenity if id """
    if amenity_id is None:
        amenities = storage.all(Amenity).values()
        return jsonify([amenity.to_dict() for amenity in amenities])
    else:
        one_amenity = storage.get(Amenity, amenity_id)
        if not one_amenity:
            abort(404)
        return jsonify(one_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deleting amenity based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({})), 200


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def add_amenity():
    """ adds new amenity on database """
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_data:
        # abort(400, 'Missing name')
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**json_data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """ updates a amenity based in amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    for k, v in json_data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
