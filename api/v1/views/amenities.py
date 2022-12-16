#!/usr/bin/python3
""" new view for Amenities objects """
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.amenity import Amenity
from flask import Flask, make_response, jsonify
import requests
from flask import request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>')
def get_amenities(amenity_id=None):
    """ Retrieves the list of all State objects """
    if amenity_id is None:
        amenities_objs = [amenity.to_dict() for amenity in
                          storage.all(Amenity).values()]
        return make_response(jsonify(amenities_objs), 200)
    else:
        obj = storage.get(Amenity, amenity_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    data = request.get_json(silent=True, force=True)
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)

    obj = Amenity(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id=None):
    if amenity_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        obj = storage.get(Amenity, amenity_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            data = request.get_json(silent=True, force=True)
            if data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(obj, item, value) for item, value in data.items()
             if item != ('id', 'created_at', 'updated_at')]
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
