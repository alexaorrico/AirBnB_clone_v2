#!/usr/bin/python3
""" View Amenity """

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"])
def amenityAll():
    """Retrieves all amenities with a list of objects"""
    all_amenities = []
    s = storage.all('Amenity').values()
    for v in s:
        all_amenities.append(v.to_dict())
    return jsonify(all_amenities)


@app_views.route("/amenities/<id>", methods=["GET"])
def amenityId(id):
    """id Amenity retrieve json object"""
    s = storage.all('Amenity').values()
    for v in s:
        if v.id == id:
            return jsonify(v.to_dict())
    abort(404)


@app_views.route("/amenities/<id>", methods=["DELETE"])
def amenityDel(id):
    """delete Amenity with id"""
    amenity = storage.get("Amenity", id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def amenityPost():
    """ POST a new amenity"""
    x = request.get_json()
    if x is None:
        abort(400, "Not a JSON")
    if not x.get('name'):
        abort(400, "Missing name")
    new_state = State(**x)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/amenities/<id>', methods=['PUT'])
def amenityPut(id):
    """ Update an amenity object """
    x = request.get_json()
    if x is None:
        abort(400, "Not a JSON")
    ignore = {"id", "created_at", "updated_at"}
    amenity = storage.get("Amenity", id)
    if amenity is None:
        abort(404)
    for k, v in x.items():
        if k not in ignore:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
