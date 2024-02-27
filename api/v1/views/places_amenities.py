#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenities_per_place(place_id=None):
    """
        reviews route to handle http method for requested reviews by place
    """
    place_obj = storage.get('Place', place_id)

    if request.method == 'GET':
        if place_obj is None:
            abort(404, 'Not found')
        all_amenities = storage.all('Amenity')
        if STORAGE_TYPE == 'db':
            place_amenities = place_obj.amenities
        else:
            place_amen_ids = place_obj.amenities
            place_amenities = []
            for amen in place_amen_ids:
                response.append(storage.get('Amenity', amen))
        place_amenities = [
            obj.to_json() for obj in place_amenities
            ]
        return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def amenity_to_place(place_id=None, amenity_id=None):
    """
        reviews route to handle http methods for given review by ID
    """
    place_obj = storage.get('Place', place_id)
    amenity_obj = storage.get('Amenity', amenity_id)
    if place_obj is None:
        abort(404, 'Not found')
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if (amenity_obj not in place_obj.amenities and
                amenity_obj.id not in place_obj.amenities):
            abort(404, 'Not found')
        if STORAGE_TYPE == 'db':
            place_obj.amenities.remove(amenity_obj)
        else:
            place_obj.amenity_ids.pop(amenity_obj.id, None)
        place_obj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (amenity_obj in place_obj.amenities or
                amenity_obj.id in place_obj.amenities):
            return jsonify(amenity_obj.to_json()), 200
        if STORAGE_TYPE == 'db':
            place_obj.amenities.append(amenity_obj)
        else:
            place_obj.amenities = amenity_obj
        return jsonify(amenity_obj.to_json()), 201
