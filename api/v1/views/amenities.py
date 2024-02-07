#!/usr/bin/python3
"""
Define route for view Amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities(amenity_id=None):
    """Retrieves a Amenity or All the amenities"""
    amenity = storage.get(Amenity, amenity_id)

    if request.method == 'GET':
        if amenity_id is not None:
            if amenity is None:
                abort(404)
            return jsonify(amenity.to_dict())
        amenities = storage.all(Amenity)
        amenities_dicts = [val.to_dict() for val in amenities.values()]
        return jsonify(amenities_dicts)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')

        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
