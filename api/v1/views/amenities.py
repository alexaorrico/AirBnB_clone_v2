#!/usr/bin/python3
"""Amenities"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getallamenities():
    """Gets all amenities"""
    res = []
    for i in storage.all("Amenity").values():
        res.append(i.to_dict())

    return jsonify(res)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getamenity(amenity_id=None):
    """Gets an amenity"""
    s = storage.get("Amenity", amenity_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteamenity(amenity_id=None):
    """Deletes an amenity"""
    s = storage.get("Amenity", amenity_id)
    if s is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createamenity():
    """Create an amenity"""
    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    elif "name" not in s.keys():
        abort(400, "Missing name")
    else:
        new_s = amenities.Amenity(**s)
        storage.new(new_s)
        storage.save()
        return jsonify(new_s.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateamenity(amenity_id=None):
    """Update an amenity"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200
