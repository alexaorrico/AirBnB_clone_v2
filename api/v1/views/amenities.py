#!/usr/bin/python3
"""ammonite colony"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, Blueprint
from models.amenity import Amenity


@app_views.route('/amenities')
def get_amenities():
    """asdasdadsa"""
    lizt = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        lizt.append(amenity.to_dict())
    return jsonify(lizt)


@app_views.route('/amenities/<amenity_id>')
def get_an_amenity(amenity_id):
    """return unique amenity"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    ret = amenities.to_dict()
    return jsonify(ret)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_an_amenity(amenity_id):
    """asdasdasdasdasd"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
