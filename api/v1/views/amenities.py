#!/usr/bin/python3
"""Amenities API"""
# Import the required modules
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity

# Route for geting all the amenities
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """GETs amenity information for all amenities"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)

# Route for getting a single amenity by its id
@app_views.route('/amenities/<string:amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """get amenity information for specified amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

# Route for deleting an amenity
@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity based on its amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)

# Route for creating a new amenity
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)

# Route for updating an existing amenity
@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict())