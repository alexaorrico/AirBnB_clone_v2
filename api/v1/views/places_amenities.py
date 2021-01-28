#!/usr/bin/python3
"""view for Placae and Amenity relationship object that
    handles all default RestFul API actions"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_of_place(place_id):
    """Retrieve the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = place.amenities
    else:
        place_amenity = place.amenity_ids

    amenity_place = [amenity.to_dict() for amenity in place_amenity]
    return jsonify(amenity_place)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity_place(place_id, amenity_id):
    """Deletes a Amenity object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = place.amenities
    else:
        place_amenity = place.amenity_ids

    if amenity not in place_amenity:
        abort(404)

    place_amenity.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenity_place(place_id, amenity_id):
    """Deletes a Amenity object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = place.amenities
    else:
        place_amenity = place.amenity_ids

    if amenity in place_amenity:
        return jsonify(amenity.to_dict()), 200

    place_amenity.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
