#!/usr/bin/python3
"""
create a new view that handles all default RESTFul API actions
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """retrieve the list of all Amenity objects"""
    # retrieve all Amenity objects
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """retrieve an Amenity object"""
    # get an Amenity object and its ID
    amenity = storage.get(Amenity, amenity_id)
    # raise an error id the amenity_id is not linked to an Amenity object
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    # raise error if the amenity_id is not linked to any Amenity object
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create an Amenity object"""
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')
    amenity = Amenity(**body)
    storage.new(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
