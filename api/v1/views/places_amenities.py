#!/usr/bin/python3
'''module for handling Place-Amenity relationships'''

from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_of_place(place_id):
    '''retrieves all Amenity objects of a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = []
    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    elif storage.__class__.__name__ == 'FileStorage':
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    '''deletes an Amenity from a Place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
        storage.save()
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity_id not in place.amenity_ids:
            abort(404)

        place.amenity_ids.remove(amenity_id)
        storage.save()

    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    '''links an Amenity to a Place'''
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()
    return jsonify(amenity.to_dict()), 201
