#!/usr/bin/python3

"""amenities.py Expose endpoints for the amenity resource"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def fetch_amenities():
    """Fetch all amenities from the store"""
    states = storage.all(Amenity).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_state_by_id(amenity_id: int):
    """Fetch a single amenity by it's ID"""
    state = storage.get(Amenity, amenity_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id: int):
    """Delete an amaenity by it's ID"""
    state = storage.get(Amenity, amenity_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Create a new amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    content = request.get_json()
    amenity = Amenity(**content)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an amenity"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    content = request.get_json()
    for key, value in content.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
