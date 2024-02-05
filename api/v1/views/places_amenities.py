#!/usr/bin/python3
"""
Module for handling RESTful API actions for
the link between Place and Amenity objects.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import *
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")

    if storage.__class__.__name__ == 'DBStorage':
        amenities = place.amenities
    elif storage.__class__.__name__ == 'FileStorage':
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()
                     if amenity.id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")
    if amenity is None:
        abort(404, description=f"Amenity with ID {amenity_id} not found")

    if storage.__class__.__name__ == 'DBStorage':
        if amenity not in place.amenities:
            abort(404, description=f"Amenity with ID {amenity_id}\
                  not linked to Place with ID {place_id}")
        place.amenities.remove(amenity)
        storage.save()
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity.id not in place.amenity_ids:
            abort(404, description=f"Amenity with ID {amenity_id}\
                  not linked to Place with ID {place_id}")
        place.amenity_ids.remove(amenity.id)
        storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")
    if amenity is None:
        abort(404, description=f"Amenity with ID {amenity_id} not found")

    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
    elif storage.__class__.__name__ == 'FileStorage':
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)
        storage.save()

    return jsonify(amenity.to_dict()), 201
