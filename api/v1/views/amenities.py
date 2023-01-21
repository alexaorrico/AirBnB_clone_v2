#!/usr/bin/python3
""" state view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


@app_views.route('/amenities', methods=["GET", "POST"], strict_slashes=False)
def get_amenities():
    """get all instances of amenity"""
    if request.method == "GET":
        response = []
        amenities = storage.all(Amenity).values()
        for amenity in amenities:
            response.append(amenity.to_dict())
        return (jsonify(response))

    if request.method == "POST":
        """post a new instance"""
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        amenity = Amenity(**new_data)
        amenity.save()
        return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """get, update an delete amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        response = amenity.to_dict()
        return (jsonify(response))
    if request.method == "PUT":
        new_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in new_data.items():
            setattr(amenity, key, value)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)
    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        response = make_response(jsonify({}), 200)
        return response
