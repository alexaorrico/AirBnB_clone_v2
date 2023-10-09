#!/usr/bin/python3
"""amenities script"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def list_all_amenities():
    '''Retrieves a list of all State objects'''
    list_amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(list_amenities)


@app_views.route('amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(name=request_data['name'])
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return make_response(jsonify({'error': 'not found'}), 404)
    request_data = request.get_json()
    if not request_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
