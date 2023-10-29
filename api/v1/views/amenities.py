#!/usr/bin/python3
"""Amenities View"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
    """Return all amenities"""
    dic_amenities = storage.all(Amenity)
    list_amenities = []
    for m in dic_amenities.values():
        list_amenities.append(m.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve amenity according to class id,
    otherwise raise 404 error
    """
    if amenity_id:
        dic_am = storage.get(Amenity, amenity_id)
        if dic_am is None:
            abort(404)
        else:
            return jsonify(dic_am.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an object Amenity if exits, otherwise 404"""
    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)
        if amenities is None:
            abort(404)
        else:
            storage.delete(amenities)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def response_amenity():
    """Post request to create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    reque = request.get_json()
    if "name" not in reque:
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenities = Amenity(**reque)
    amenities.save()
    return make_response(jsonify(amenities.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates attributes from an Amenity obj"""
    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)
        if amenities is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        reque = request.get_json()
        for key, value in reque.items():
            if key not in ['id', 'created_at', 'update_at']:
                setattr(amenities, key, value)
        amenities.save()
        return make_response(jsonify(amenities.to_dict()), 200)
