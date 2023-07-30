#!/usr/bin/python3
""" Objects that handles all default RESTFul API actions for amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieve list of all amenity objects. """
    all_amenities = storage.all(Amenity).values()
    list_amenities  = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to-dict())
    return jsonify(list_amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """ Creates an amenity object. """ 
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', method=['PUT'], strict_slashes=False)
def put_amenities(amenity_id):
    """ Updates a Amenity object. """
    if not request.get_json():
        abort(400, description='Not a JSON')

    ignore = ['id', 'created_at', 'updated_at']
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort (404)

    data = request.get_json()
    for key, value in data.items():
        if key in ignore:
            setattr(amenity, key, value)
    
    storage.save()
    return jsonify(amenity.to_dict()), 200
            