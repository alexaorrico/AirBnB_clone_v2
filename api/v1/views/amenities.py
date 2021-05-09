#!/usr/bin/python3
"""Amenities"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getallamenities():
    """Gets all amenities"""
    res = []
    for i in storage.all(Amenity).values():
        res.append(i.to_dict())

    return jsonify(res)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getamenity(amenity_id):
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
    s = request.get_json()
    if s is None:
        return jsonify("Not a JSON"), 400
    elif 'name' not in s:
        return jsonify("Missing name"), 400
    else:
        new_s = Amenity(**s)
        new_s.save()
        return jsonify(new_s.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateamenity(amenity_id):
    """Update an amenity"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        return jsonify("Not a JSON"), 400
    else:
        for k, v in s.items():
            if k in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, k, v)
        storage.save()
        res = obj.to_dict()
        return jsonify(res), 200
