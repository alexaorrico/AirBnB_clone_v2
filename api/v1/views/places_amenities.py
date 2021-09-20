#!/usr/bin/python3
"""View between Place objects and Amenity"""

import models
from flask import jsonify, abort
from flask import request as req
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities')
def place_amenity_objects(place_id):
    """Methods for places by place_id"""
    place = models.storage.get('Place', place_id)
    if place is None:
        abort(404)

    amenities = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'])
def place_amenity_res(place_id, amenity_id):
    """Methods for amenities by place_id and amenity_id"""
    place = models.storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = models.storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    amenity_linked = False
    for a in place.amenities:
        if a.id == amenity.id:
            amenity_linked = True
            break
    if not amenity_linked:
        abort(404)

    if req.method == 'DELETE':
        if models.storage_t == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.rewmove(amenity.id)
        models.storage.save()
        return jsonify({})

    if req.method == 'POST':
        if amenity_linked:
            return jsonify(amenity.to_dict()), 200

        if models.storage_t == 'db':
            place.amenities.push(amenity)
        else:
            place.amenity_ids.push(amenity.id)
        models.storage.save()
        return jsonify(amenity.to_dict()), 201
