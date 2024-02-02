#!/usr/bin/python3
'''View to handle the RESTful API actions for 'Amenity' objects'''
from flask import jsonify, request, abort

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    '''Handles "/amenities" route'''
    if request.method == 'GET':
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
        return jsonify(amenities)

    if request.method == 'POST':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400
        name = data.get('name')
        if name is None:
            return 'Missing name', 400
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def amenity_actions(amenity_id):
    '''Handles actions for "/amenities/<amenity_id>" route'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None or type(data) is not dict:
            return 'Not a JSON', 400
        for attr, val in data.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, attr, val)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
