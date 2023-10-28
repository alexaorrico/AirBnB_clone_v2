#!/usr/bin/python3
"""Contains all REST actions for amenity Objects"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """retrieves a amenities objects"""
    amenity = storage.all(Amenity)
    all_amenities = []
    for i in amenity.values():
        all_amenities.append(i.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def get_amenity(id):
    """retrieves a amenity objects"""
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(id):
    """deletes a amenity objects"""
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """creates a amenity objects"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    data = request.get_json()
    amenity = Amenity(**data)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def put_amenity(id):
    """updates a amenity objects"""
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ['id', 'created_at', 'updated_at']
    if 'name' in request.get_json():
        amenity.name = request.get_json()['name']
    amenity.save()
    return jsonify(amenity.to_dict()), 200
