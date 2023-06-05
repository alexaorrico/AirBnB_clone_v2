#!/usr/bin/python3
"""route handler for Amenity object"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
@app_views.route('/amenities/<amenity_id>')
def amenity_index(amenity_id=None):
    """GET method handler for amenities"""
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())
    else:
        amenities = storage.all(Amenity).values()
        amenities = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def amenity_delete(amenity_id):
    """DELETE method handler for amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities', methods=["POST"])
def amenity_post():
    """POST method handler for amenity object"""
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()

    if data.get('name') is None:
        return "Missing name", 400
    name = data.get('name')
    amenity = Amenity()
    amenity.name = name
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    """
    PUT handler for updating a amenity object
    """
    if not request.is_json:
        return "Not a JSON", 400
    data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        return abort(404)

    for key, value in data.items():
        if key in ('id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
