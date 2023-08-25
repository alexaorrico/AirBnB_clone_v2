#!/usr/bin/python3
"""
new view for Amenity objects that handles all default RESTFul API actions
"""
from models import storage
from models.amenity import Amenity

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieve the list all amenities"""
    all_amenities = []
    amenities = storage.all("Amenity").values()
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves amenity object"""
    all_amenities = []
    amenities = storage.all("Amenity").values()
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    for a in all_amenities:
        if a.get("id") == amenity_id:
            return jsonify(a)
    abort(404)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity"""
    amenities = storage.all("Amenity")
    try:
        key = 'Amenity.' + amenity_id
        storage.delete(amenities[key])
        storage.save()
        return jsonify({}), 200
    except BaseException:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """creates a Amenity"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    else:
        request_body = request.get_json()
    if 'name' not in request_body:
        abort(400, 'Missing name')
    else:
        amenity = Amenity(**request_body)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """updates a Amenity"""
    amenities = storage.all(Amenity)
    key = 'Amenity.' + amenity_id
    try:
        amenity = amenities[key]
    except keyError:
        abort(404)
    if request.is_json:
        request_body = request.get_json()
    else:
        abort(400, 'Not a JSON')
    for key, value in request_body.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
