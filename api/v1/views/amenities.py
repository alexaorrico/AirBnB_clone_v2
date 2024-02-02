#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities/', methods=["GET"])
def amenities_get():
    """Get all amenity objects"""
    array = []

    all_obj = storage.all(Amenity)

    for obj in all_obj.values():
        dictionary = obj.to_dict()
        array.append(dictionary)

    return jsonify(array)


@app_views.route("/amenities/<obj_id>", methods=["GET"])
def amenity_get(obj_id):
    """Get a amenity object"""
    obj = storage.get(Amenity, obj_id)

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/amenities/<obj_id>", methods=["DELETE"])
def amenity_delete(obj_id):
    """Delete a amenity object"""
    obj = storage.get(Amenity, obj_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def amenity_create():
    """Create a new Amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, "Missing name")

    new_obj = Amenity(**data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/amenities/<obj_id>', methods=['PUT'])
def amenity_update(obj_id):
    """Update a Amenity object"""
    obj = storage.get(Amenity, obj_id)
    if obj is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict()), 200
