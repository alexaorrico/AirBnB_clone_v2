#!/usr/bin/python3
''' REST API blueprint for Amenity class '''

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    ''' returns all amenity objects in JSON formart '''
    amenities = [amen.to_dict() for amen in storage.all('Amenity').values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_using_id(amenity_id):
    ''' returns amenity with maching id '''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    ''' deletes an amenity object given its amenity_id '''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    ''' creates a new amenity object '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        amenity = Amenity(**data)
        amenity.save()
        return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenities_id):
    ''' updates an existing amenity object '''
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity = storage.get("Amenity", amenities_id)
    if amenity is None:
        abort(404)
    for attr, value in data:
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, value)
    obj.save()
    return (jsonify(amenity.to_dict()), 200)
