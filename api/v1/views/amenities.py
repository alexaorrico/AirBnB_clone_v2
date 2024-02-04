#!/usr/bin/python3
"""
module for CRUD Amenity object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ retrieve the list of amenities"""
    all_am = storage.all(Amenity).values()
    amenities = [am.to_dict() for am in all_am]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """retrieve specif amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """ remove amenity from storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ create new amenity """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    obj_amenity = Amenity(**data)
    obj_amenity.save()
    return jsonify(obj_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ update amenity based on amenity_id"""
    ref_obj_amenity = storage.get(Amenity, amenity_id)
    if not ref_obj_amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key in data:
        if key not in ['id', 'created_at', 'updated_at']:
            # ref_obj_state.__dict__[key] = data[key]
            setattr(ref_obj_amenity, key, data[key])
    storage.save()
    return jsonify(ref_obj_amenity.to_dict()), 200
