#!/usr/bin/python3
'''This module Retrieves the list of all review objects,
deletes, updates, creates and gets information of a review '''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models import storage
import models


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_all_amenities_in_place(place_id):
    ''' retreive all amenities associated with the place id '''
    place = storage.get(Place, place_id)

    if place and models.storage_t == 'db':
        return jsonify([obj.to_dict() for obj in place.amenities])
    if place:
        amenity_objs = []
        for amenity_id in place.amenity_ids:
            amenity_objs.append(storage.get(Amenity, amenity_id))
        return jsonify([obj.to_dict() for obj in amenity_objs])
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities_in_place(place_id, amenity_id):
    '''Remove the ameniry object from the amenities relationship in place
    object'''
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)

    if not place_obj or not amenity_obj:
        abort(404)
    if amenity_obj not in place_obj.amenities:
        abort(404)
    if models.storage_t == 'db':
        place_obj.amenities.remove(amenity_obj)
    else:
        place_obj.amenity_ids.remove(amenity_id)
    place_obj.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenities(place_id, amenity_id):
    ''' link an  amenity it to the place id'''
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)

    if not place_obj or not amenity_obj:
        abort(404)
    if amenity_obj not in place_obj.amenities:
        abort(404)

    if amenity_obj in place_obj.amenities:
        return jsonify(amenity_obj.to_dict()), 200

    if models.storage_t != 'db':
        place_obj.amenity_ids.append(amenity_id)
    else:
        place_obj.amenities.append(amenity_obj)
    place_obj.save()
    return jsonify(amenity_obj.to_dict()), 201
