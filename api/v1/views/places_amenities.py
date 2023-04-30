#!/usr/bin/python3
'''
place amenities
'''
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from os import getenv
# index


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_allamens(place_id):
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if not place.amenities:
        return jsonify([])
    return jsonify([amen.to_dict() for amen in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def place_amenity(place_id, amenity_id):
    amen = storage.get('Amenity', amenity_id)
    place = storage.get('Place', place_id)
    if not amen or not place:
        abort(404)

    if request.method == 'DELETE':
        if amen not in place.amenities:
            abort(404)
        storage.delete(amen)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amen not in place.amenities:
            place.amenities.append(amen)
            place.save()
            return jsonify(amen.to_dict()), 201
        return jsonify(amen.to_dict()), 200
