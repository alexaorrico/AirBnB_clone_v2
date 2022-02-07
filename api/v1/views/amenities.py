#!/usr/bin/python3
"""
module for amenity views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all("Amenity")
    result = []
    for amenity in amenities.values():
        result.append(amenity.to_dict())
    return jsonify(result)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an Amenity object """
    amenities = storage.all("Amenity")
    for key in amenities.keys():
        if key.split('.')[-1] == amenity_id:
            return jsonify(amenities.get(key).to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenities = storage.all("Amenity")
    for key in amenities.keys():
        if key.split('.')[-1] == amenity_id:
            storage.delete(amenities.get(key))
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Creates an Amenity """
    dic = request.get_json()
    if not dic:
        abort(400, "Not a JSON")
    if not ('name' in dic.keys()):
        abort(400, "Missing name")
    amenity = Amenity(**dic)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates an Amenity object """
    amenities = storage.all("Amenity")
    amenity = None
    for key in amenities.keys():
        if key.split('.')[-1] == amenity_id:
            amenity = amenities.get(key)
    if not amenity:
        abort(404)
    new_dict = request.get_json()
    if not new_dict:
        abort(400, "Not a JSON")
    for key, value in new_dict.items():
        if key in ('id', 'created_at', 'updated_at'):
            continue
        else:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
