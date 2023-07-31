#!/usr/bin/python3
"""RESTful API for linking Place and Amenity objects"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route(
    '/places/<place_id>/amenities',
    methods=['GET'],
    strict_slashes=False)
def get_place_amenities(place_id):
    '''
        Retrieves the list of all Amenity objects of a Place
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenities_list = [a.to_dict() for a in place.amenities]
    return jsonify(amenities_list)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    '''
        Deletes an Amenity object to a Place
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['POST'],
    strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    '''
        Links an Amenity object to a Place
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
