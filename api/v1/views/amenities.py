#!/usr/bin/python3
""" amenities function """

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


# GET all amenities
# ============================================================================

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ get amenities object """
    amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(list_amenities)


# GET 1 amenity
# ============================================================================

@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ amenity object """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


# DELETE an amenity
# ============================================================================

@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity if not exist """

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# CREATE an amenity
# ============================================================================

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ create an amenity """

    json_request = request.get_json()

    if json_request is None:
        abort(400, 'Not a JSON')

    if 'name' not in json_request:
        abort(400, 'Missing name')

    amenity = Amenity(**json_request)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


# UPDATE an amenity
# ============================================================================

@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update city by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'state_id', 'create_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
