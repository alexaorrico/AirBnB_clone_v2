#!/usr/bin/python3
"""Amenit documented"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities_list():
    """returns all amenities"""
    amenities_found = storage.all(Amenity)
    if amenities_found is None:
        abort(404)
    amenities_list = []
    for key, object in amenities_found.items():
        amenities_list.append(object.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity(amenity_id):
    """returns amenity of id given"""
    amenity_found = storage.get(Amenity, amenity_id)
    if amenity_found is None:
        abort(404)
    return jsonify(amenity_found.to_dict()), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenities():
    """create an amenity"""
    http_request = request.get_json(silent=True)
    if http_request is None:
        return 'Not a JSON', 400
    elif 'name' not in http_request.keys():
        return 'Missing name', 400
    new_amenity = Amenity(**http_request)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """updates given amenity"""
    found_amenity = storage.get(Amenity, amenity_id)
    if found_amenity is None:
        return '', 404
    http_request = request.get_json(silent=True)
    if http_request is None:
        return 'Not a JSON', 400
    for key, values in http_request.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(found_amenity, key, values)
    storage.save()
    return jsonify(found_amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id):
    """delete amenity if id is found"""
    amenity_found = storage.get(Amenity, amenity_id)
    if amenity_found is None:
        return '{}', 404
    storage.delete(amenity_found)
    storage.save()
    return jsonify({}), 200
