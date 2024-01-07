#!/usr/bin/python3
"""
Creates a view for Amenity objects - handles all default RESTful API actions.
"""
from flask import abort, jsonify, request
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    amenities = storage.all(Amenity).values()"""convert object ot dictionary"""
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
"""Retrieves an Amenity object"""


def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)"""Return 404 error if the Amenity object is not found"""


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
"""
Deletes an Amenity object'''
Get the Amenity object with the given ID from the storage
"""


def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()"""returns 200 code"""
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
"""
Creates an Amenity object
Return 400 error if the request data is not in JSON format
"""


def create_amenity():
    if not request.get_json():
        abort(400, 'Not a JSON')
        data = request.get_json()
        if 'name' not in data:
            abort(400, 'Missing name')
            """ Create a new Amenity object with the JSON data"""
            amenity = Amenity(**data)
            amenity.save()
            """
            Return the newly created Amenity
            object in JSON format with 201 status code
            """
            return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
"""
Updates an Amenity object
Get the Amenity object with the given ID from the storage
"""


def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')
            """Get the JSON data from the request"""
            data = request.get_json()
            ignore_keys = ['id', 'created_at', 'updated_at']
            """update amenity attributes"""
            for key, value in data.items():
                if key not in ignore_keys:
                    setattr(amenity, key, value)
                    amenity.save()
                    return jsonify(amenity.to_dict()), 200
                else:
                    abort(404)
