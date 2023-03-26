#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""
from flask import jsonify
from flask import abort
from flask import request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """Retrieves the list of all Amenity objects"""
    try:
        amenity = storage.all(Amenity)
        AmenityList = []
        for k in amenity:
            AmenityList.append(amenity[k].to_dict())
        return jsonify(AmenityList)
    except:
        abort(404)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'])
def getAmenity(amenity_id):
    """Retrieves a Amenity object"""
    try:
        amenity = storage.get(Amenity, amenity_id).to_dict()
        return jsonify(amenity)
    except:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def deleteAmenity(amenity_id):
    """Deletes a Amenity object"""
    try:
        storage.delete(Amenity, amenity_id)
        storage.save()
        return {}, 200
    except:
        abort(404)


@app_views.route("/amenities", methods=['POST'], endpoint='amenitysPost')
def postAmenity():
    """Creates a Amenity"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    instance = Amenity(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def putAmenity(amenity_id):
    """Updates a Amenity object"""
    k = "Amenity." + str(amenity_id)
    if k not in storage.all():
        abort(404)
    data = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(storage.all()[k], key, value)
    storage.all()[k].save()
    return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200
