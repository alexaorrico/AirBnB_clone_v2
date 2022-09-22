#!/usr/bin/python3
"""
flask application module for retrieval of
Amenity Objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models.exceptions import *


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_amenity():
    """Retrieves the list of all Amenity objects"""
    return (jsonify(Amenity.api_get_all()), 200)


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """Creates a Amenity"""
    try:
        return (jsonify(
            Amenity.api_post(
                request.get_json(silent=True))),
                201)
    except BaseModelMissingAttribute as attr:
        return (jsonify({'error': 'Missing {}'.format(attr)}), 400)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """handles get Amenity object: amenity_id"""
    try:
        return (jsonify(
            Amenity.api_get_single(amenity_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """handles Amenity object: amenity_id"""
    try:
        return (jsonify(
            Amenity.api_delete(amenity_id)), 200)
    except BaseModelInvalidObject:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_amenity_by_id(amenity_id):
    """handles update of Amenity object: amenity_id"""
    try:
        return (Amenity.api_put(
                request.get_json(silent=True),
                amenity_id), 200)
    except BaseModelInvalidDataDictionary:
        return (jsonify({'error': "Not a JSON"}), 400)
    except BaseModelInvalidObject:
        abort(404)
