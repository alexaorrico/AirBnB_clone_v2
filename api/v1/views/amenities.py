#!/usr/bin/python3
"""
amenity
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_full_amenity_method():
    new_dict = []
    for obj in storage.all(Amenity).values():
        new_dict.append(obj.to_dict())
    return jsonify(new_dict)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_method(amenity_id):
    amnit = storage.get(Amenity, amenity_id)
    if amnit is None:
        abort(404)
    return jsonify(amnit.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_method(amenity_id):
    if amenity_id is None:
        abort(404)
    amnit = storage.get(Amenity, amenity_id)
    if amnit is None:
        abort(404)
    amnit.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity_method():
    res = request.get_json()
    if not isinstance(res, dict):
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in res:
        return abort(400, {'message': 'Missing name'})
    new_amnit = Amenity(**res)
    new_amnit.save()
    return jsonify(new_amnit.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity_method(amenity_id):
    amnit = storage.get(Amenity, amenity_id)
    if amnit is None:
        abort(404)
    res = request.get_json()
    if not isinstance(res, dict):
        return abort(400, {'message': 'Not a JSON'})
    for key, value in res.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amnit, key, value)
    storage.save()
    return jsonify(amnit.to_dict()), 200
