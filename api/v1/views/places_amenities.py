#!/usr/bin/python3
"""
Module for Place object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_to_a_place(place_id):
    """ Retrieves the list of all amenities of a place """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        amenities_list = []
        for amenity in place_obj.amenities:
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list), 200
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE']
)
def delete_amenity_to_a_place(place_id, amenity_id):
    """ Delete a amenity to a place object """
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place_obj and amenity_obj:
        if amenity_obj in place_obj.amenities:
            place_obj.amenities.remove(amenity_obj)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE']
)
def link_amenity_to_a_place(place_id, amenity_id):
    """ Link a amenity to a place object """
    place_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)
    if place_obj and amenity_obj:
        if amenity_obj not in place_obj.amenities:
            place_obj.amenities.append(amenity_obj)
            storage.save()
        return jsonify(amenity_obj.to_dict()), 200
    else:
        abort(404)
