#!/usr/bin/python3
"""creates a new view for State Objects"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_for_place(place_id=None):
    """get place information for all places in a specified city"""
    obj = storage.get(Place, place_id)
    if obj is None:
        return jsonify({}), 404
    lis = []
    for pos in obj.amenities:
        lis.append(pos.to_dict())
    return jsonify(lis), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_to_place(place_id=None, amenity_id=None):
    """deletes"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    lis = storage.get(Amenity, amenity_id)
    if lis is None:
        abort(404)
    if lis not in obj.amenities:
        abort(404)
    else:
        storage.delete(lis)
        storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_to_place(place_id=None, amenity_id=None):
    """linker"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    lis = storage.get(Amenity, amenity_id)
    if lis is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        obj_amenities = obj.amenities
    else:
        obj_amenities = obj.amenity_ids
    if amenity in obj_amenities:
        return jsonify(amenity.to_dict())
    obj_amenities.append(amenity)
    obj.save()
    return make_response(jsonify(amenity.to_dict()), 201)
