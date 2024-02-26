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
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    des_am = []
    if storage_t == 'db':
        des_am = [am.to_dict() for am in place.amenities]
    else:
        for id in place.amenity_ids:
            obj = storage.get(Amenity, id)
            if obj is not None:
                des_am.append(obj.to_dict())
    return jsonify(des_am)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_o(place_id, amenity_id):
    """
    delete one
    """
    place = storage.get(Place, place_id)
    sup_am = storage.get(Amenity, amenity_id)
    if place is None or sup_am is None:
        abort(404)
    if storage_t == 'db':
        if sup_am in place.amenities:
            place.amenities.remove(sup_am)
            storage.save()
            return jsonify({}), 200
    else:
        if sup_am.id in place.amenity_ids:
            place.amenity_ids.remove(sup_am.id)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    only links
    """
    place = storage.get(Place, place_id)
    sup_am = storage.get(Amenity, amenity_id)
    if place is None or sup_am is None:
        abort(404)
    if storage_t == 'db':
        if sup_am not in place.amenities:
            place.amenities.append(sup_am)
            storage.save()
            return jsonify(sup_am.to_dict()), 201
    else:
        if sup_am.id not in place.amenity_ids:
            place.amenity_ids.append(sup_am.id)
            storage.save()
            return jsonify(sup_am.to_dict()), 201
    return jsonify(sup_am.to_dict()), 200
