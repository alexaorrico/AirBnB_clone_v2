#!/usr/bin/python3
"""adasda"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models import amenity
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAmenity():
    """aaasdasdasd"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenityById(amenity_id):
    """asdasdasda"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """asdasdasda"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def createAmenity():
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    if json_req.get("name") is None:
        abort(400, 'Missing name')
    new_obj = State(**json_req)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    json_req = request.get_json()
    if json_req is None:
        abort(400, 'Not a JSON')
    for key, value in json_req.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
