#!/usr/bin/python3

""" Module handling requests for Amenity objects """

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET', 'POST'])
def all_amenity():
    """ Handles GET and POST request for all amenities """
    if request.method == 'GET':
        amenity_objects = storage.all(Amenity)
        amenity_list = []
        for key, val in amenity_objects.items():
            amenity_list.append(val.to_dict())
        return jsonify(amenity_list)

    if request.method == 'POST':
        data = request.get_json(silent=True)
        amenity = Amenity()
        if data is None:
            return 'Not a JSON', 400
        if 'name' not in data.keys():
            return 'Missing name', 400
        ignored_keys = ['id', 'created_at', 'updated_at']
        for key in data:
            if key not in ignored_keys:
                setattr(amenity, key, data[key])
        amenity.save()
        return(amenity.to_dict()), 201
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    """ Handles GET, DELETE and PUT requests for amenity by id """
    if request.method == 'GET':
        amenity_objects = storage.all(Amenity)
        for key, val in amenity_objects.items():
            if val.id == amenity_id:
                return val.to_dict()
        abort(404)

    if request.method == 'DELETE':
        amenity_objects = storage.all(Amenity)
        for key, val in amenity_objects.items():
            if val.id == amenity_id:
                storage.delete(val)
                storage.save()
                return {}, 200
        abort(404)

    if request.method == 'PUT':
        try:
            valid_request = request.get_json()
        except Exception:
            return 'Not a JSON', 400

        ignored_keys = ['id', 'created_at', 'updated_at']
        amenity_objects = storage.all(Amenity)
        for key, val in amenity_objects.items():
            if val.id == amenity_id:
                for key in valid_request:
                    if key not in ignored_keys:
                        setattr(val, key, valid_request[key])
                storage.save()
                return val.to_dict(), 200
        abort(404)
