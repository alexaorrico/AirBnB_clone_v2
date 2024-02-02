#!/usr/bin/python3
"""Module with a flask script"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City

@app_views.route('/cities/', methods=["GET"])
def cities_get():
    """Get all city objects"""
    array = []

    all_obj = storage.all(City)

    for obj in all_obj.values():
        dictionary = obj.to_dict()
        array.append(dictionary)

    return jsonify(array)


@app_views.route("/cities/<obj_id>", methods=["GET"])
def city_get(obj_id):
    """Get a city object"""
    obj = storage.get(City, obj_id)

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/cities/<obj_id>", methods=["DELETE"])
def city_delete(obj_id):
    """Delete a city object"""
    obj = storage.get(City, obj_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/', methods=['POST'])
def city_create():
    """Create a new City"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'name' not in data:
        abort(400, "Missing name")

    new_obj = City(**data)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/cities/<obj_id>', methods=['PUT'])
def city_update(obj_id):
    """Update a City object"""
    obj = storage.get(City, obj_id)
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
