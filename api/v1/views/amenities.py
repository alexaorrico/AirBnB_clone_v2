#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def all_amenities():
    """liste all amenities"""
    list_amenities = []
    all_amenities = storage.all(Amenity).values()
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """get one amenity"""
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ Delete a amenity"""
    if amenity_id is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """add a amenity"""
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    if 'name' not in requeste.keys():
        abort(400, "Missing name")
    new_amenity = Amenity(**requeste)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id=None):
    """update a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    for key, value in requeste.items():
        setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
