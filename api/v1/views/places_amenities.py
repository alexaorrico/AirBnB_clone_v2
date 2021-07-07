#!/usr/bin/python3
"""view of State object"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort


@app_views.route('/places/<place_id>/amenities', methods=["GET"])
def ame_ret(place_id=None):
    """return json Amenity objects"""
    ame_list = []
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    for obj in place_obj.amenities:
        ame_list.append(obj.to_dict())
    return jsonify(ame_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE"])
def ame_delete(place_id=None, amenity_id=None):
    """delete an object by id"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    ame_obj = storage.get("Amenity", amenity_id)
    if ame_obj is None:
        abort(404)
    for place_ame_obj in place_obj.amenities:
        if place_ame_obj.id == amenity_id:
            place_obj.amenities.remove(place_ame_obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=["POST"])
def post_ame_obj(place_id=None, amenity_id=None):
    """add new state object"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    ame_obj = storage.get("Amenity", amenity_id)
    if ame_obj is None:
        abort(404)
    for place_ame_obj in place_obj.amenities:
        if place_ame_obj.id == amenity_id:
            return jsonify(ame_obj.to_dict()), 200
    place_obj.amenities.append(ame_obj)
    storage.save()
    return jsonify(ame_obj.to_dict()), 201
