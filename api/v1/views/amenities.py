#!/usr/bin/python3
"""
    Flask route that returns json respone
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, class_richard


@app_views.route('/amenities/', methods=['GET'])
def amenities_no_id(amenity_id=None):
    """amenities route - no id GET scenario"""
    all_amenities = storage.all('Amenity')
    all_amenities = [obj.to_dict() for obj in all_amenities.values()]
    return jsonify(all_amenities)

@app_views.route('/amenities/', methods=['POST'])
def amenities_no_id(amenity_id=None):
    """amenities route - no id POST scenario"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get('name') is None:
        abort(400, 'Missing name')
    Amenity = class_richard.get('Amenity')
    new_object = Amenity(**req_json)
    new_object.save()
    return jsonify(new_object.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_with_id(amenity_id=None):
    """amenities route - id given scenario"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity_obj.to_dict())

    if request.method == 'DELETE':
        amenity_obj.delete()
        del amenity_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        amenity_obj.save(req_json)
        return jsonify(amenity_obj.to_dict()), 200
