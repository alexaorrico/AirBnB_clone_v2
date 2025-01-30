#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import make_response
from flask import request
from flask import jsonify


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAmenities():
    """retrieve the list of all Amenity objects"""
    all_amenities = storage.all(Amenity)

    list_amenities = [val.to_dict() for val in all_amenities.values()]
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenity(amenity_id):
    """retrieve Amenity object"""
    all_amn = storage.all(Amenity)
    for val in all_amn.values():
        if val.id == amenity_id:
            return jsonify(val.to_dict())
    return make_response({"error": "Not found"}, 404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """delete a Amenity object"""
    all_amn = storage.all(Amenity)
    for val in all_amn.values():
        if val.id == amenity_id:
            storage.delete(val)
            storage.save()
            return make_response(jsonify({}), 200)
    return make_response({"error": "Not found"}, 404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """create a Amenity object"""
    all_amn = storage.all(Amenity)
    new_amn = Amenity()
    try:
        data = request.get_json()
        if "name" not in data:
            return make_response("Missing name", 400)
        for key, val in data.items():
            setattr(new_amn, key, val)
            storage.new(new_amn)
            storage.save()
            return make_response(jsonify(new_amn.to_dict()), 201)
    except Exception as e:
        return make_response("Not a JSON", 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """update Amenity object"""
    all_amn = storage.all(Amenity)
    all_ids = []
    for val in all_amn.values():
        all_ids.append(val.id)
    if amenity_id not in all_ids:
        return make_response(jsonify({"error": "Not found"}), 404)
    try:
        data = request.get_json()
        for v in all_amn.values():
            if amenity_id == v.id:
                for key, value in data.items():
                    setattr(v, key, value)
                storage.save()
                return make_response(jsonify(v.to_dict()), 200)
    except Exception as e:
        return make_response("Not a JSON", 400)
