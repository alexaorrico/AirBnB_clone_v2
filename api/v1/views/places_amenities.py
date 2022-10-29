#!/usr/bin/python3
"""
a view for the link between Place objects and Amenity objects that
handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

@app_views.route('/places/<string:place_id>/amenities', methods=['GET'])
def getPlaceAmenities(place_id):
    """
    get amenity information for a specified place otherwise 404
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        amenities = []
        if STORAGE_TYPE == 'db':
            amenityObjs = place.amenities
        else:
            amenityObjs = place.amenity_ids
        for amenity in amenityObjs:
            amenities.append(amenity.to_dict())
        return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', methods=['DELETE', 'POST'])
def ManagePlaceAmenity(place_id, amenity_id):
    """
    Delete and update place_amenity information
    """
    place_obj = storage.get('Place', place_id)
    amenity_obj = storage.get('Amenity', amenity_id)
    if place_obj is None or amenity_obj is None:
        abort(404)

    if request.method == 'DELETE':
        if STORAGE_TYPE == 'db':
            place_amenities = place.amenities
        else:
            place_amenities = place.amenity_ids
        if amenity_obj not in place_amenities:
            abort(404)
        place_amenities.remove(amenity_obj)
        place_obj.save()
        return jsonify({})

    if request.method == 'POST':
        if STORAGE_TYPE == 'db':
            place_amenities = place.amenities
        else:
            place_amenities = place.amenity_ids
        if amenity_obj in place_amenities:
            return jsonify(amenity_obj.to_dict())
        place_amenities.append(amenity_obj)
        place_obj.save()
        return make_response(jsonify(amenity_obj.to_dict()), 201)
