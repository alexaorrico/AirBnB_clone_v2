#!/usr/bin/python3
"""amenity module"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenity", methods=['GET'], strict_slashes=False)
def all_amenity():
    """return json"""
    for amenity in storage.all(Amenity).values():
        all_amenity = amenity.to_dict()
    return jsonify(all_amenity)


@app_views.route("/amenity/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def all_amenity_by_id(amenity_id):
    """return json"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return jsonify(abort(404))


@app_views.route("/amenity/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenity_by_id(amenity_id):
    """return json"""
    amenity = storage.get(Amenity, amenity_id)
    if Amenity is None:
        return jsonify(abort(404))
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenity", methods=['POST'], strict_slashes=False)
def post_amenity():
    """return json"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 404)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 404)
    amenity = request.get_json()
    am = Amenity(**amenity)
    am.save()
    return jsonify(am.to_dict()), 201


@app_views.route("/amenity/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity_by_id(amenity_id):
    """return json"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify(abort(404))
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
