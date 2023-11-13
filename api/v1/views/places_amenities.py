#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""view for the link between Place objects and Amenity\
objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid

# GET /places/<place_id>/amenities


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)

# DELETE /places/<place_id>/amenities/<amenity_id>


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_place(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200

# POST /places/<place_id>/amenities/<amenity_id>


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_by_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

# GET /places/<place_id>/amenities/<amenity_id>


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_place(place_id, amenity_id):
    """Retrieves a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    return jsonify(amenity.to_dict()), 200

# GET /amenities/<amenity_id>/places


@app_views.route('/amenities/<amenity_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_amenity(amenity_id):
    """Retrieves the list of all Place objects of a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    places = []
    for place in amenity.places:
        places.append(place.to_dict())
    return jsonify(places)

# DELETE /amenities/<amenity_id>/places/<place_id>


@app_views.route('/amenities/<amenity_id>/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_amenity(amenity_id, place_id):
    """Deletes a Place object to a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place not in amenity.places:
        abort(404)
    amenity.places.remove(place)
    storage.save()
    return jsonify({}), 200

# POST /amenities/<amenity_id>/places/<place_id>


@app_views.route('/amenities/<amenity_id>/places/<place_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_by_amenity(amenity_id, place_id):
    """Link a Place object to a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place in amenity.places:
        return jsonify(place.to_dict()), 200
    amenity.places.append(place)
    storage.save()
    return jsonify(place.to_dict()), 201

# GET /amenities/<amenity_id>/places/<place_id>


@app_views.route('/amenities/<amenity_id>/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_amenity(amenity_id, place_id):
    """Retrieves a Place object to a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place not in amenity.places:
        abort(404)
    return jsonify(place.to_dict()), 200
