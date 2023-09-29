#!/usr/bin/python3
"""API endpoints for cities"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


def get_amenity_or_abort(amenity_id):
    """Retrieve an object by ID or abort with 404 if not found"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return amenity


def create_amenity(data):
    """Create a new amenity in the database."""
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return new_amenity


def validate_json():
    """Validate that the request data is in JSON format."""
    try:
        return request.get_json()
    except Exception:
        abort(400, "Not a JSON")


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities():
    """Route for manipulating Amenity objects"""

    if request.method == 'GET':
        # Get a list of all Amenity objects
        amenities = storage.all(Amenity)
        amenities_list = [amenity.to_dict() for amenity in amenities.values()]
        return jsonify(amenities_list)

    if request.method == 'POST':
        # Add a State to the list
        data = validate_json()
        if "name" not in data:
            abort(400, "Missing name")
        new_amenity = create_amenity(data)
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def amenity_with_id(amenity_id=None):
    """Route for manipulating a specific City object"""

    amenity = get_amenity_or_abort(amenity_id)

    if request.method == 'GET':
        # Get a specific state by id
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        # Delete a specific state by id
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        # Update a specific state by id
        data = validate_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
