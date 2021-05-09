#!/usr/bin/python3

"""
Create a new view for State objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAll():
    """Retrieve all objects"""
    l = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(l)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get(amenity_id):
    """Retrieve an object by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(amenity_id):
    """Delete a state object by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        obj.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create():
    """Create an object"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    name = body.get('name')
    if not name:
        abort(400, "Missing name")

    obj = Amenity(**body)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update(state_id):
    """Update an object"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
