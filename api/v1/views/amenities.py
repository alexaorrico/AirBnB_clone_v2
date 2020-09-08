#!/usr/bin/python3
"""ammonite colony"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity


@app_views.route('/api/v1/amenities')
def get_amenities():
    """asdasdadsa"""
    lizt = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        lizt.append(amenity.to_dict())
    return jsonify(lizt)


@app_views.route('/api/v1/amenities/<amenity_id>')
def get_an_amenity():
    """return unique amenity"""
    lizt = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        if amenity.id == amenity_id:
            lizt = amenity.to_dict()
            return jsonify(lizt)
    return jsonify({"error": "Not found"}), 404


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['DELETE'])
def del_an_amenity():
    """asdasdasdasdasd"""
    water_pressure = storage.all(Amenity).values()
    for amenity in water_pressure:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404
