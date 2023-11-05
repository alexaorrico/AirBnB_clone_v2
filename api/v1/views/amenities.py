#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def all_amenity():
    """return json"""
    list_amenity = []
    for amenity in storage.all(Amenity).values():
        list_amenity.append(amenity.to_dict())
    return jsonify(list_amenity)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def all_amenity_by_id(amenity_id):
    """return json"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_amenities_by_id(amenity_id):
    """return json"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity():
    """return json"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = request.get_json()
    ame = Amenity(**amenity)
    ame.save()
    return make_response(jsonify(ame.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_amenity_by_id(amenity_id):
    """return json"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
