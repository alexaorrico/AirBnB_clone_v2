#!/usr/bin/python3
"""A new view for the link between Places objects and Amenity
objects that handles all default RESTFUL API actions"""


from flask import Flask, jsonify, request, abort
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import getenv

store = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenity_by_place_id(place_id):
    """Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = [a.to_dict() for a in place.amenities]
    return jsonify(amenities), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """Delete amenity object from a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    for elements in place.amenities:
        if elements.id == amenity.id:
            if store == 'db':
                place.amenities.remove(amenity)
            else:
                place.amenity_ids.remove(amenity)
            place.save()
            return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Link an amenity object to a place
    """
    lists = []
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    for element in place.amenities:
        if element.id == amenity.id:
            return jsonify(amenity.to_dict()), 200
    if store == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_id.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
