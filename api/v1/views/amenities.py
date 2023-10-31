#!/usr/bin/python3
'''
    Create a new view for Amenity objects that handles
    all default RESTFul API actions
'''
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    '''Retrieves Amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity =  storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''Creates Amenity Object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    jsonData = request.get_json()
    if 'name' not in jsonData:
        abort(400, 'Missing name')
    amenity = Amenity(**jsonData)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates Amenity Object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            abort(400, 'Not a JSON')
        jsonData = request.get_json()
        ignoreKeys = ['id', 'created_at', 'updated_at']
        for key, value in jsonData.items():
            if key not in ignoreKeys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(400)
def bad_request(error):
    '''Bad request message handler'''
    res = {'error': 'Bad Request'}
    return jsonify(res), 400