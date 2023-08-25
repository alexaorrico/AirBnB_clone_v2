#!/usr/bin/python3
"""Handles default RESTFul API actions to create a
new view fo the link between Place objects and Amenity objects"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, CNC
from models.place import Place
from models.amenity import Amenity
from os import environ
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route(
        '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    all_amenities = storage.all('Amenity')
    if STORAGE_TYPE == 'db':
        place_amenities = place.amenities
    else:
        place_amen_ids = place.amenities
        place_amenities = []
        for a in place_amen_ids:
            response.append(storage.get('Amenity', a))
    place_amenities = [
            obj.to_json() for obj in place_amenities]
    return jsonify(place_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=[
    'DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    if STORAGE_TYPE == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.pop(amenity.id, None)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=[
    'POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)

    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if STORAGE_TYPE == 'db':
        place.amenities.append(amenity)
    else:
        place.amenities = amenity
        storage.save()
        return jsonify(amenity.to_json()), 201
