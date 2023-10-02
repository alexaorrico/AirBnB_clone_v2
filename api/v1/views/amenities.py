#!/usr/bin/python3
"""
The amenities module
"""
from models import storage
from flask import Blueprint, jsonify, request, abort
from models.amenity import Amenity

amenities_bp = Blueprint('amenities', __name__, url_prefix='/api/v1/amenities')


@amenities_bp.route('/', methods=['GET'], strict_slashes=False)
def get_amenities():
    amenities = [a.to_dict() for a in storage.all(Amenity).values()]
    return jsonify(amenities)


@amenities_bp.route('/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@amenities_bp.route('/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenities(amenity_id):
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return jsonify({})


@amenities_bp.route('/', methods=['POST'], strict_slashes=False)
def create_amenities():
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')
    new_amenities = Amenity(**data)
    new_amenities.save()
    return jsonify(new_amenities.to_dict()), 201


@amenities_bp.route('/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenities(amenity_id):
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenities, key, value)
    amenities.save()
    return jsonify(amenities.to_dict())
