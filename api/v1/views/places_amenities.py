#!/usr/bin/python3
"""
Handle all default RESTFUL API actions
"""
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify
from models import storage


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def places_amenities(place_id):
    """ Returns infor for places reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities = []
        for amenity in place.amenities:
            amenities.append(amenity.to_dict())
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def place_amenity(place_id, amenity_id):
    """ Returns review object of id """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if request.method == 'POST':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200
