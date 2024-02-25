#!/usr/bin/python3
"""
amenities.py
"""
from . import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from flask import abort, request, make_response, Response
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """
    Retrieves the list of all amenity objects
    """
    dict_of_amenities = [obj.to_dict()
                         for obj in storage.all(Amenity).values()]
    response = Response(
        response=json.dumps(dict_of_amenities, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Retrieves a Amenity object:
    GET /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Deletes an amenity object::
    DELETE /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    creates amenity
    """
    if not request.is_json:
        return make_response('Not a JSON', 400)
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    updates an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    ignored_keys = ['id', 'updated_at', 'created_at']
    for key, value in data.items():
        if key in ignored_keys:
            continue
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
