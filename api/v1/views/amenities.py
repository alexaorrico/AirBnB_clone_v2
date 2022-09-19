#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_get():
    """Retrieves the list of all Amenity"""
    amenities_list = []
    all_amenities = storage.all(Amenity)
    for key, value in all_amenities.items():
        amenities_list.append(value.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_post():
    """Creates a Amenity"""
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    if 'name' not in transform_dict.keys():
        abort(400, "Missing name")
    else:
        new_amenity = Amenity(**transform_dict)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id_get(amenity_id):
    """Retrieves a Amenity object and 404 if it's an error"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_id_delete(amenity_id):
    """Deletes a Amenity object and 404 if it's an error"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_id_put(amenity_id):
    """Updates a Amenity object"""
    ignore_list = ['id', 'created_at', 'updated_at']
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    transform_dict = request.get_json()
    if transform_dict is None:
        abort(400, "Not a JSON")
    for key, value in transform_dict.items():
        if key not in ignore_list:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
