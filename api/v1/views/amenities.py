#!/usr/bin/python3
"""
handles all default RestFul API actions for amenities
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """
    get all the amenities
    """
    list_objects = []

    if amenity_id is None:
        for item in storage.all(Amenity).values():
            list_objects.append(item.to_dict())

        return jsonify(list_objects)
    else:
        data = storage.get(Amenity, amenity_id)
        if data is None:
            abort(404)
        return jsonify(data.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """
    delete aminity by id
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    """
    create amenities
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    json_data = request.get_json()
    if "name" not in json_data:
        abort(400, "Missing name")

    new_amenity = Amenity(**json_data)
    storage.new(new_amenity)
    storage.save()

    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """
    update the amenity by id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    json_data = request.get_json()
    if "name" not in json_data:
        abort(400, "Missing name")

    for key, value in json_data.items():
        if key not in ["id", "updated_at", "created_at"]:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict())
