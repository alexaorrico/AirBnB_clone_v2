#!/usr/bin/python3
"""This handles all default RESTFul API actions for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """Retrieves list of all Amenity objects"""
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrieves an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates an Amenity object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if data.get('name', None) is None:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """updates Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for p, q in data.items():
        if p not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, p, q)
    amenity.save()
    return jsonify(amenity.to_dict())
