#!/usr/bin/python3
"""Amenity view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects
    """
    return jsonify([amenity.to_dict()
                   for amenity in storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity(amenity_id):
    """Retrieves a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return amenity.to_dict()


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity
    """
    amenity = request.get_json()
    if amenity is None:
        abort(400, "Not a JSON")
    if "name" not in amenity:
        abort(400, "Missing name")
    amenity = Amenity(**amenity)
    amenity.save()
    return amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_json = request.get_json()
    if amenity_json is None:
        abort(400, "Not a JSON")
    for key, value in amenity_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return amenity.to_dict(), 200
