#!/usr/bin/python3
"""Amenity module """
from models.amenity import Amenity
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """Returns a list of amenities"""

    all_amenities = []

    for amenity in storage.all("Amenity").values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/cities/<amenity_id>')
def get_method_amenity(state_id):
    """Returns an instance of the specified object"""
    amenity = storage.get("Amenity", amenity_id)
    if city is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_method_amenity(amenity_id):
    """deletes amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete()
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/amenities', methods=['POST'])
def create_amenities(state_id):
    """creates specified test"""

    if not request.get_json():
        return abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        return abort(400, description="Missing name")

    amenity = Amenity()
    Amenity.name = request.get_json().get['name']
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """updates city method"""
    if not request.get_json():
        return abort(400, description="Not a JSON")

    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(amenity, key, value)
    storage.save()

    return make_response(jsonify(amenity.to_dict(), 200))
