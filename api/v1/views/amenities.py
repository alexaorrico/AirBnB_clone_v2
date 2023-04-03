#!/usr/bin/python3
"""Flask route module for amenities"""
from api.v1.views import app_views, validate_model
from flask import abort, jsonify, request
from models import storage, classes


@app_views.route('/amenities/', methods=['GET'])
def amenities_no_id_get(amenity_id=None):
    """amenities route - no id GET scenario"""
    all_amenities = storage.all('Amenity')
    all_amenities = [obj.to_dict() for obj in all_amenities.values()]
    return jsonify(all_amenities)

@app_views.route('/amenities/', methods=['POST'])
def amenities_no_id_post(amenity_id=None):
    """amenities route - no id POST scenario"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get('name') is None:
        abort(400, 'Missing name')
    Amenity = classes.get('Amenity')
    new_object = Amenity(**req_json)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_with_id_get(amenity_id=None):
    """amenities route - id given GET scenario"""
    amenity_obj = validate_model('Amenity', amenity_id)
    return jsonify(amenity_obj.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenities_with_id_del(amenity_id=None):
    """amenities route - id given DELETE scenario"""
    amenity_obj = validate_model('Amenity', amenity_id)
    storage.delete(amenity_obj)
    return jsonify({}), 200

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenities_with_id_put(amenity_id=None):
    """amenities route - id given PUT scenario"""
    amenity_obj = validate_model('Amenity', amenity_id)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    for key, value in req_json.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
