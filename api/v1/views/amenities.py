#!/usr/bin/python3
""" Amenity RESTful API """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Uses to_dict to retrieve an object into a valid JSON """
    all_amenities = storage.all("Amenity")
    list = []
    for amenity in all_amenities.values():
        list.append(amenity.to_dict())
        print(amenity)
    return jsonify(list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def individual_amenities(amenity_id):
    """ Retrieves an Amenity object, or returns a 404 if the amenity_id is not
    linked to any object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object, or returns a 404 if the amenity_id is not
    linked to any object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity object, or returns a 400 if the HTTP body request is not
    valid JSON, or if the dict doesnt contain the key name """
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    name = data.get("name")
    if name is None:
        abort(400, "Missing name")
    new_amenity = Amenity()
    new_amenity.name = name
    new_amenity.save()
    return (jsonify(new_amenity.to_dict())), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an Amenity object, or returns a 400 if the HTTP body is not valid
    JSON, or a 404 if state_id is not linked to an object """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return (jsonify(amenity.to_dict()))
