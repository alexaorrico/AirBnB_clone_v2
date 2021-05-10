#!/usr/bin/python3
""" new view for Amenity """
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def allamenities():
    """ GET all amenities """
    res = []
    for i in storage.all("Amenity").values():
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def getamenities(amenity_id=None):
    """ GET amenities """
    s = storage.get("Amenity", amenity_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def deleteamenity(amenity_id=None):
    """ DELETE amenity """
    s = storage.get("Amenity", amenity_id)
    if s is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['CREATE'], strict_slashes=False)
def createamenity():
    """ CREATE amenity """
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "None a JSON")
    elif "name" not in s.keys():
        abort(400, "Missing name")
    else:
        new_s = amenities.Amenity(**s)
        storage.new(new_s)
        storage.save()
        return jsonify(new_s.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def updateamenity(amenity_id=None):
    """ Update amenity with PUT """
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
