#!/usr/bin/python3
"""city flask triggers"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def allamenities():
    """retrieve all amenities"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenityobj(amenity_id):
    """retrieves an object of amenity"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenitydelete(amenity_id):
    """deletes an amenity object"""
    amenobj = storage.get(Amenity, amenity_id)
    if amenobj is None:
        abort(404)
    storage.delete(amenobj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def amenitycreate():
    """create and object amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "missing name"}), 400)
    jsoncity = Amenity(**request.get_json())
    jsoncity.save()
    return make_response(jsonify(jsoncity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenityupdate(amenity_id):
    """update an amenity as json"""
    update_amen = storage.get(Amenity, amenity_id)
    if update_amen is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(update_amen, key, value)
    update_amen.save()
    return jsonify(update_amen.to_dict()), 200
