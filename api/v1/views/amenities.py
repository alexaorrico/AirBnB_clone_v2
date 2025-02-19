#!/usr/bin/python3
"""RESTful API for class Amenity"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenities.yml', methods=['GET'])
def get_amenities():
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def post_amenity():
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    if 'name' not in res:
        return abort(400, description="Missing name")
    new_amenity = Amenity(**res)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def put_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    res = request.get_json()
    if not res:
        return abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200

