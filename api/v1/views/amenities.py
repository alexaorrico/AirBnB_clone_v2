#!/usr/bin/python3
""" a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """retrieves the list of all Amenity objects
    """
    if request.method == "GET":
        all_amenities = []
        for key in storage.all("Amenity").values():
            all_amenities.append(key.to_dict())
        return jsonify(all_amenities)

    if request.method == 'POST':
        if not request.is_json:
            return "Not a JSON", 400
        all_amenities = Amenity(**request.get_json())
        if "name" not in all_amenities.to_dict().keys():
            return "Missing name", 400
        all_amenities.save()
        return all_amenities.to_dict(), 201


@app_views.route('/amenity/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """updates a state object
    """
    if request.method == "GET":
        amenity_info = storage.get(Amenity, amenity_id)
        if amenity_info is not None:
            return amenity_info.to_dict()
        abort(404)

    if request.method == "PUT":
        amenity_info = storage.get(Amenity, amenity_id)
        if amenity_info is not None:
            if not request.is_json:
                return "Not a JSON", 400
            for k, v in request.get_json().items():
                setattr(amenity_info, k, v)
            storage.save()
            return amenity_info.to_dict()
        abort(404)

    if request.method == "DELETE":
        amenity_info = storage.get(Amenity, amenity_id)
        if amenity_info:
            amenity_info.delete()
            storage.save()
            return {}, 200
        abort(404)
