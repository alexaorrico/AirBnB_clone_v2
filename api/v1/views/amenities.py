#!/usr/bin/python3
"""amenities objects that handles all default RESTFul API actions
"""
from flask import request, jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities.py', methods=['GET'])
def retrive_amenity():
    """ retrieves the list of all City
    """
    amenities = storage.all(Amenity).value()
    list_amenity = []
    for amenity in amenities:
        list_amenity.append(amenity.to_dict())
    return jsonify(list_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def retrive_amenities_id(amenity_id):
    """Retrives amenity id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), status=200)


@app_views.route('/amenities', methods=['POST'])
def post_amenity(state_id):
    """ request post for amenity
    """
    amenity = storage.get(Amenity, state_id)
    data = request.get_json()

    if not data:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)
    else:
        new_amenity = Amenity(**data)
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """ request put for amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()
    key_ignore = ['id', 'state_id', 'created_at', 'updated_at']
    if not amenity:
        abort(404)
    elif not data:
        return (jsonify({'error': 'Not a JSON'}), 400)
    else:
        for key, value in data.items():
            if key not in key_ignore:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
