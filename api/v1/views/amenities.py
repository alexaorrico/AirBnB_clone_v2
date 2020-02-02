#!/usr/bin/python3
""" Create a new view for State that handles all default RestFul API """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def Amenity_Get():
    """Retrieves the list of all Amenity objects """
    data = storage.all('Amenity')
    amenity = []

    for value in data.values():
        amenity.append(value.to_dict())
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def Amentity_Id(amenity_id):
    """ Retrieves a Amenity object """
    data = storage.all('Amenity')
    for key, value in data.items():
        key = key.split(".")
        if key[-1] == amenity_id:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def Amenity_Delete(amenity_id):
    """ Deletes a Amenity object """
    data = storage.all('Amenity')
    del_amenity = storage.get('Amenity', amenity_id)
    if del_amenity is None:
        abort(404)
    storage.delete(del_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def Amenities_Post():
    """ Creates a Amenity """

    data = request.get_json()

    if not data:
        return jsonify({"message": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"message": "Missing name"}), 400

    name_amenity = {"name": data["name"]}
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def Amenity_Put(amenity_id):
    """ Updates a Amenity object """

    data = storage.get('Amenity', amenity_id)
    data_req = request.get_json()

    if data is None:
        abort(404)
    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400

    for key, value in data_req.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200
