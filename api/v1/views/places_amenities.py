#!/usr/bin/python3
"""Default RESTFul API for Place-Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity
import json
import models

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def place_id_amenity(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    Creates an Amenity
    """
    if models.storage_t == 'db':
        if request.method == 'GET':
            place = storage.get(Place, place_id)
            if place:
                single_objs = []
                for amenity in place.amenities:
                    single_objs.append(amenity.to_dict())
                return jsonify(single_objs)
            abort(404)
    else:
        if request.method == 'GET':
            place = storage.get(Place, place_id)
            if place:
                single_objs = []
                for amenity in place.amenity_ids:
                    single_objs.append(amenity.to_dict())
                return jsonify(single_objs)
            abort(404)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'], strict_slashes=False)
def place_id_amenity_id(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if request.method == 'DELETE':
            for amen in place.amenities:
                if amenity_id == amen.id:
                    new_dict = {}
                    amen.delete()
                    storage.save()
                    return jsonify(new_dict), 200
        if request.method == 'POST':
            for amen in place.amenities:
                if amenity_id == amen.id:
                    return jsonify(amen.to_dict()), 200
            setattr(place, 'amenity_id', amenity_id)
            return jsonify(amen.to_dict()), 201 
    abort(404)