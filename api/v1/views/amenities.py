#!/usr/bin/python3
""" This module contains the amenities view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_amenities():
    """ Retrieves the list of all Amenity objects """
    if request.method == 'GET':
        amenities = storage.all('Amenity')
        return jsonify([amenity.to_dict() for amenity in amenities.values()])
    elif request.method == 'POST':
        req_json = request.get_json()
        if not req_json:
            abort(400, 'Not a JSON')
        if 'name' not in req_json:
            abort(400, 'Missing name')
        amenity = Amenity(**req_json)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def handle_amenity(amenity_id=None):
    """ Retrieves an Amenity object """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200
