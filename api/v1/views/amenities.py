#!/usr/bin/python3
"""
a new view for Amenities objects
that handles all default RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ retrieves the list of all amenity objects """
    amenities = storage.all(Amenity).values()
    json_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(json_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ retrieves a amenity object (specified with amenity_id) """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletes a amenity object (specified with amenity_id) """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ creates an amenity object """
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    if 'name' not in amenity_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updates a State object (specified with state_id) """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, "Not a JSON")
    for key, value in amenity_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
