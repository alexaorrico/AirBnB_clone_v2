#!/usr/bin/python3
"""View for Amenities"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
    """Return amenities"""
    dict_am = storage.all(Amenity)
    list_am = []
    for v in dict_am.values():
        list_am.append(v.to_dict())
    return jsonify(list_am)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenities(amenity_id):
    """Return amenity for class and  Amenit id or return error message
    """
    if amenity_id:
        dict_am = storage.get(Amenity, amenity_id)
        if dict_am is None:
            abort(404)
        else:
            return jsonify(dict_am.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes one Amenity if exists, or erros message 404
    """
    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)
        if amenities is None:
            abort(404)
        else:
            storage.delete(amenities)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def response_amenity():
    """create a new amenity if exists the class or raise Error
        if is not a valid json or if the name is missing
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenities = Amenity(**req)
    amenities.save()
    return make_response(jsonify(amenities.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """Updates attributes for Amenity"""
    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)
        if amenities is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        request = request.get_json()
        for k, v in request.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenities, k, v)
        amenities.save()
        return make_response(jsonify(amenities.to_dict()), 200)
