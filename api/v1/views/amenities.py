#!/usr/bin/python3
""" Handle amenity API"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrive all amenities object"""
    allAmenitys = storage.all(Amenity).values()
    amenitiesList = []
    for amenity in allAmenitys:
        amenitiesList.append(amenity.to_dict())
    return jsonify(amenitiesList)


@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def get_amenity(id):
    """retrive amenity object with a particular id"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(id):
    """Delete a amenity object"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    res = request.get_json()
    if type(res) != dict:
        abort(400, "Not a JSON")
    if "name" not in res:
        abort(400, "Missing name")
    amenity = Amenity(**res)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    amenity = storage.get(Amenity, id)
    if not amenity:
        abort(404)
    res = request.get_json()
    if not res:
        abort(400, "Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for item in res:
        if item not in ignore:
            setattr(amenity, item, res[item])
    storage.save()
    return jsonify(amenity.to_dict()), 200
