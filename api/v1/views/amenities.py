#!/usr/bin/python3
""" amenities """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


@app_views.route('/amenities', methods=["GET", "POST"],
                 strict_slashes=False)
def get_all_amenities():
    """ retrieves all amenity objects """
    output = []
    amenities = storage.all(Amenity).values()
    if request.method == "GET":
        for amenity in amenities:
            output.append(amenity.to_dict())
        return (jsonify(output))
    if request.method == "POST":
        data = request.get_json()
        if not request.is_json():
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        amenity = Amenity(**data)
        amenity.save()
        return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=[
                 "GET", "PUT", "DELETE"], strict_slashes=False)
def get_an_amenity(amenity_id):
    """ retrieves one unique amenity object """
    amenitiy = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        output = amenity.to_dict()
        return (jsonify(output))
    if request.method == "PUT":
        data = request.get_json()
        if not request.is_json():
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(amenity, key, value)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        result = make_response(jsonify({}), 200)
        return result
