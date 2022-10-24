#!/usr/bin/python3
'''contains amenity routes'''
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    '''retrieves amenity objects'''
    amenity_list = [a.to_dict() for a in storage.all(Amenity).values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'])
def get_amenity_id(amenity_id):
    '''returns amenity with given id'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    '''deletes amenity object using amenity_id'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenities():
    '''create new amenity obj'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    else:
        obj_data = request.get_json()
        obj = Amenity(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'])
def update_amenity(amenities_id):
    '''update existing amenity object'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get(Amenity, amenities_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
