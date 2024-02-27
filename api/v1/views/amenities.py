#!/usr/bin/python3
"""
Creates a new view for the cities class, and can also handle the RESTful API
PROCESSES
"""
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """
    used to get amenity objects, on requests
    """
    user_output = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        user_output.append(amenity.to_dict())
    return (jsonify(user_output))


@app_views.route('/amenities', methods=["GET", "POST"], strict_slashes=False)
def create_amenity():
    """
    class used to create a new amenity
    """
    amenity_data = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    amenity = Amenity(**amenity_data)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=[
                 "GET", "PUT"], strict_slashes=False)
def get_single_amenity(amenity_id):
    """class to retrieve a unique amenity object with specified
    ID
    """
    defined_amenity = storage.get(Amenity, amenity_id)
    if defined_amenity is None:
        abort(404)
    if request.method == "GET":
        output = defined_amenity.to_dict()
        return (jsonify(output))
    if request.method == "PUT":
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in user_data.items():
            setattr(defined_amenity, key, value)
        defined_amenity.save()
        return (jsonify(defined_amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def remove_single_amenity(amenity_id):
    """ 
    used to delete a unique amenity with defined ID
    """
    defined_amenity = storage.get(Amenity, amenity_id)
    if defined_amenity is None:
        abort(404)
    storage.delete(defined_amenity)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
