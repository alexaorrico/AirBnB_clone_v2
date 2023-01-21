#!/usr/bin/python3
""" Amenity view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ list all Amenity object """
    output = []
    amenities = storage.all(Amenity).values()
    for value in amenities:
        output.append(value.to_dict())
    return (jsonify(output))


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def create_amenity():
    """creates a new amenity """
    data = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def an_amenity(amenity_id):
    """ Retrieves an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        output = amenity.to_dict()
        return (jsonify(output))
    if request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(amenity, key, value)
        amenity.save()
        return (jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ Deletes an amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
