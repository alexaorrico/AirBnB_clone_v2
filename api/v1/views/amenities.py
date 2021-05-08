#!/usr/bin/python3
"""Amenity views"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities_get():
    """Retrieves the list of all Amenity objects"""
    all_amenity = storage.all('Amenity')
    amenity_for_json = []
    for amenity in all_amenity.values():
        amenity_for_json.append(amenity.to_dict())
    return jsonify(amenity_for_json)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenities(amenity_id):
    """Retrieves an Amenity object"""
    all_amenities = storage.get('Amenity', amenity_id)
    if all_amenities is None:
        abort(404)
    return jsonify(all_amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """Deletes an Amenity object"""
    if not storage.get('Amenity', amenity_id):
        abort(404)
    else:
        storage.get('Amenity', amenity_id).delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """Creates an Amenity"""
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    new_amenities = Amenity(name=request.json["name"])
    storage.new(new_amenities)
    storage.save()
    return jsonify(new_amenities.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id):
    """Updates an Amenity object"""
    req = request.get_json()
    if not request.json:
        abort(400, "Not a JSON")
    amenity_to_modify = storage.get('Amenity', amenity_id)
    if amenity_to_modify is None:
        abort(404)
    for key in req:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_to_modify, key, req[key])
    storage.save()
    return jsonify(amenity_to_modify.to_dict()), 200
