#!/usr/bin/python3
"""
a view for amenity objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'])
def get_add_amenities():
    """
    get and create Amenity objects
    """
    amenityObj = storage.all("Amenity")
    if request.method == 'GET':
        amenities = []
        for amenity in amenityObj.values():
            amenities.append(amenity.to_dict())
        return jsonify(amenities)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        kwargs = request.get_json()
        amenity = Amenity(**kwargs)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def manageAmenities(amenity_id):
    """
    manipulate Amenity information with specific ID
    """
    amenityObj = storage.get("Amenity", amenity_id)
    if amenityObj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenityObj.to_dict())

    if request.method == 'DELETE':
        amenityObj.delete()
        storage.save()
        return (jsonify({}))

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(amenityObj, attr, val)
        amenityObj.save()
        return jsonify(amenityObj.to_dict())
