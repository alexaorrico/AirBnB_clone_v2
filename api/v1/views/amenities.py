#!/usr/bin/python3
"""A view for Amenity objects that handles all default RESTFul API actions"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response

@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET', 'POST'])
def amenities():
    """Retrieves the list of all Amenity objects"""
    if request.method == 'GET':
        return jsonify([amenity.to_dict() for amenity in
                        storage.all(Amenity).values()])

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_amenity = Amenity(**request.get_json())
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenities_id(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
