"""Module providing API endpoints for Amenity resources."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve a list of all amenities."""
    amenities_list = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities_list)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve information about a specific amenity."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity by its ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity."""
    if request.is_json:
        data = request.get_json()
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400

        amenity = Amenity(**data)
        storage.new(amenity)
        storage.save()

        return jsonify(amenity.to_dict()), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Update an amenity's information."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.is_json:
        data = request.get_json()
        keys_to_ignore = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(amenity, key, value)
        amenity.save()

        return jsonify(amenity.to_dict()), 200
    else:
        return jsonify({"error": "Not a JSON"}), 400
