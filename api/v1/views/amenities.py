#!/usr/bin/python3
"""Creating amenities Flask app"""

from flask import Flask, jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
import json


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """gets a list of all amenities"""
    if request.method == "GET":
        allAmenities = []
        for key in storage.all("Amenity").values():
            allAmenities.append(key.to_dict())
        return jsonify(allAmenities)

    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400

        allAmenities = Amenity(**request.get_json())
        if "name" not in allAmenities.to_dict().keys():
            return "Missing name", 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def amenities_id(amenity_id):
    """Updates an amenities objects id"""
    if request.method == 'GET':
        amenity_data = storage.get(Amenity. amenity_id)
        if amenity_data is not None:
            return jsonify(amenity_data.to_dict())
        abort(404)

    if request.method == "PUT":
        amenity_data = storage.get(Amenity, amenity_id)
        if amenity_data is not None:
            if not request.is_json:
                return "Not a JSON", 400

            for k, v in request.get_json().items():
                setattr(amenity_data, k, v)
            storage.save()
            return jsonify(amenity_data.to_dict())
        abort(404)

    if request.method == "DELETE":
        amenity_data = storage.get(Amenity, amenity_id)
        if amenity_data:
            amenity_data.delete()
            storage.save()
            return jsonify({}), 200
        abort(404)
