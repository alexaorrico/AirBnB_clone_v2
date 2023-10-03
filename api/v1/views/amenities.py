#!/usr/bin/python3
"""
This Module contains Amenity objects
that handles all default RESTFul API actions
"""
from flask import Flask, abort, make_response, request, jsonify
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves a list all amenities objects """
    amenities_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """This retrieves the an amenity based of its ID """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a amenity object based on a given ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a new amenity """
    request_json = request.get_json()
    required_key = "name"

    if not request_json:
        abort(400, "Not a JSON")
    if required_key not in request_json:
        abort(400, "Missing name")

    amenity = Amenity(**request_json)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ this update an amenity object based on its amenity ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    request_json = request.get_json()
    if not request_json:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
