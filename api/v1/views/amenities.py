#!/usr/bin/python3
"""
Create a flask app that will serve the API, views module
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Return amenities
    """
    amenities_list = []
    for key, value in storage.all(Amenity).items():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Return amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def post_amenity():
    """
    Create amenity
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if data is None:
        return abort(400, 'Not a JSON')
    if 'name' not in data:
        return abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """
    Update amenity
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
