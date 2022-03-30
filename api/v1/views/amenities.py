#!/usr/bin/python3
"""HTTP methods for Amenity"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,  methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id=None):
    """
    Retrieves list of all Amenity objects
    retrieves an Amenity object
    """
    if amenity_id is None:
        list_amenity = []
        objects = storage.all('Amenity')
        for obj in objects.values():
            list_amenity.append(obj.to_dict())
        return(jsonify(list_amenity))
    else:
        id_amenity = storage.get('Amenity', amenity_id)
        if id_amenity:
            return (jsonify(id_amenity.to_dict()))
        else:
            abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id=None):
    """
    Delete an Amenity object
    """
    id_amenity = storage.get('Amenity', amenity_id)
    if id_amenity:
        storage.delete(id_amenity)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False,  methods=['POST'])
def post_amenity():
    """
    Post an amenity
    """
    dict_request = request.get_json()
    if dict_request is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in dict_request:
        return (jsonify({'error': 'Missing name'}), 400)

    new_obj = Amenity(**dict_request)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def put_amenity(amenity_id=None):
    """
    Update an amenity
    """
    update_dict = request.get_json()
    if update_dict is None:
        return (jsonify({'error': 'Not a JSON'}), 400)

    id_amenity = storage.get('Amenity', amenity_id)
    if id_amenity:
        for key, value in update_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(id_amenity, key, value)
        id_amenity.save()
        return (jsonify(id_amenity.to_dict()), 200)
    else:
        abort(404)
