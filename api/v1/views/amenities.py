#!/usr/bin/python3
"""
Handles all default RESTful API actions for Amenity objects
"""

from . import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, make_response, request
from flask.json import jsonify

AMENITY_IGNORE_KEYS = {'id', 'created_at', 'updated_at'}


@app_views.route("/amenities", methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    return jsonify([a.to_dict() for a in storage.all('Amenity').values()])


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an amenity given its ID"""
    a = storage.get('Amenity', amenity_id)
    if a is None:
        abort(404)
    return jsonify(a.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def del_amenity(amenity_id):
    """Deletes an amenity given its ID"""
    a = storage.get('Amenity', amenity_id)
    if a is None:
        abort(404)
    a.delete()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'])
def post_amenity():
    """Creates an amenity"""
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    if 'name' not in r:
        abort(make_response(jsonify("Missing name"), 400))
    a = Amenity(**r)
    a.save()
    return make_response(jsonify(a.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def put_amenity(amenity_id):
    """Updates an Amenity at a given ID"""
    a = storage.get('Amenity', amenity_id)
    if a is None:
        abort(404)
    r = request.get_json()
    if r is None:
        abort(make_response(jsonify("Not a JSON"), 400))
    for k, v in r.items():
        if k not in AMENITY_IGNORE_KEYS:
            setattr(a, k, v)
    a.save()
    return make_response(jsonify(a.to_dict()), 200)
