#!/usr/bin/python3
"""
places_amenities.py
"""
from . import app_views
from flask import jsonify
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User
from flask import abort, request, Response, make_response
import json


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities_per_place_o(place_id):
    """
    amenities depending on storage
    """
    if not storage.get(Place, place_id):
        abort(404)
    place = storage.get(Place, place_id)
    des_am = []
    if storage_t == 'db':
        des_am = [am.to_dict() for am in place.amenities]
    else:
        for id in place.amenity_ids:
            if storage.get(Amenity, id):
                obj = storage.get(Amenity, id)
                des_am.append(obj.to_dict())
    return jsonify(des_am)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_o(place_id, amenity_id):
    """
    delete one
    """
    if not storage.get(Place, place_id) or \
            not storage.get(Amenity, amenity_id):
        abort(404)
    place = storage.get(Place, place_id)
    sup_am = storage.get(Amenity, amenity_id)
    isFound = False
    if storage_t == 'db':
        for am in place.amenities:
            if am == sup_am:
                isFound = True
    else:
        for am_id in place.amenity_ids:
            if am_id == sup_am.id:
                isFound = True
    if isFound:
        storage.delete(sup_am)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    only links
    """
    if not storage.get(Place, place_id):
        abort(404)
    place = storage.get(Place, place_id)
    des_am = []
    if storage_t == 'db':
        des_am = [am.to_dict() for am in place.amenities]
    else:
        for id in place.amenity_ids:
            if storage.get(Amenity, id):
                obj = storage.get(Amenity, id)
                des_am.append(obj.to_dict())
    return jsonify(des_am)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_o(place_id, amenity_id):
    """
    delete one
    """
    if not storage.get(Place, place_id) or \
            not storage.get(Amenity, amenity_id):
        abort(404)
    place = storage.get(Place, place_id)
    sup_am = storage.get(Amenity, amenity_id)
    isFound = False
    if storage_t == 'db':
        for am in place.amenities:
            if am == sup_am:
                isFound = True
        if not isFound:
            place.amenities.append(sup_am)
            storage.save()
            return jsonify(sup_am.to_dict()), 201
    else:
        for am_id in place.amenity_ids:
            if am_id == sup_am.id:
                isFound = True
        if not isFound:
            place.amenity_ids.append(sup_am.id)
            return jsonify(sup_am.to_dict()), 201
    if isFound:
        return jsonify(sup_am.to_dict()), 200
