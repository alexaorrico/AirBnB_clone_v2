#!/usr/bin/python3
'''
    Amenity route for the API
'''
from flask import Flask
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/amenities", methods=["GET"])
def get_amenitys():
    """get amenity information for all amenitys"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenitys_by_id(amenity_id):
    """get amenity information for specific amenitys"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes a amenity based on its amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ create a amenity"""
    createJson = request.get_json()
    if createJson is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in createJson.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**createJson)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """update a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr != 'id' or attr != 'created_at' or attr != 'updated_at':
            setattr(amenity, attr, val)
    storage.save()
    return jsonify(amenity.to_dict())
