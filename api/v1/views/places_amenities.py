#!/usr/bin/python3

'''
This module create a new view for Amenity objects handling all default
RestFul API actions
Routes:
    GET : /api/v1/places/<place_id>/amenities -
        Retrieves the list of all Amenity
    DELETE : /api/v1/places/<place_id>/amenities/<amenity_id> -
        Deletes a Amenity
    POST : /api/v1/places/<place_id>/amenities/<amenity_id> -
        Link a Amenity object to a Place
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def find_amenities(place_id=None):
    '''
    Retrieves the list of all Amenity objects of a Place
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def delete_place_amen(amenity_id):
    '''
    Deletes an amenity object
    '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        if STORAGE_TYPE == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200
    '''
    POST: Link a Amenity object to a Place
    '''
    if request.method == 'POST':
        if STORAGE_TYPE == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
