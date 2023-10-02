#!/usr/bin/python3
"""
New view for Amenity objects that handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify
from api.v1.views import app_views
from models import storage, Amenity

# Route to retrieve a list of all Amenity objects
@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Get info about all amenities"""
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)

# Route to retrieve a specific Amenity object by amenity_id
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Get info about a specific amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

# Route to delete a specific Amenity object by amenity_id
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete specific amenity object using its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

# Route to create a new Amenity object
@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a new amenity object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    
    new_amenity = Amenity(**data)
    new_amenity.save()
    
    return jsonify(new_amenity.to_dict()), 201

# Route to update a specific Amenity object by amenity_id
@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a specific amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    # Ignore keys: id, created_at, updated_at
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    
    amenity.save()
    
    return jsonify(amenity.to_dict()), 200
