#!/usr/bin/python3
"""Create a new view for amenitie objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import request, abort, jsonify
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenitiesWithId(amenity_id=None):
    """Methods that retrieves all methods for amenities with id"""
    amenitieId = storage.get(Amenity, amenity_id)
    if request.method == 'GET':
        if amenitieId is None:
            return abort(404)
        return jsonify(amenitieId.to_dict())

    if request.method == 'DELETE':
        if amenitieId is None:
            return abort(404)
        amenitieId.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        if amenitieId is None:
            return abort(404)
        if request.get_json() is None:
            return abort(400, 'Not a JSON')
        toIgnore = ["id", "created_at", "updated_it"]
        for key, value in request.get_json().items():
            if value not in toIgnore:
                setattr(amenitieId, key, value)
        amenitieId.save()
        return jsonify(amenitieId.to_dict()), 200


@app_views.route('/amenities', methods=['POST', 'GET'], strict_slashes=False)
def amenitiesNoId():
    """Methods that retrieves all methods for amenities without id"""
    if request.method == 'POST':
        if request.get_json() is None:
            return abort(400, 'Not a JSON')
        if request.get_json().get('name') is None:
            return abort(400, 'Missing name')
        newamenitie = Amenity(**request.get_json())
        newamenitie.save()
        return jsonify(newamenitie.to_dict()), 201

    if request.method == 'GET':
        allAmenit = storage.all(Amenity)
        amenity = list(allObject.to_dict() for allObject in allAmenit.values())
        return jsonify(amenity)
