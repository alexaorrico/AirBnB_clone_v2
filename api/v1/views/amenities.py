#!/usr/bin/python3
"""
View for `Amenity` objects that handles all default RESTFul API actions
"""
from models import storage
from flask import jsonify, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views, Amenity


@app_views.route("/amenities", strict_slashes=False)
def get_amenity_objects():
    """returns: list of all amenities objects"""
    amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in amenities.values():
        amenity_list.append(amenity.to_dict())
    return amenity_list


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity_obj(amenity_id):
    """returns: amenity object based on its id"""
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    # amenity object not found
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_obj(amenity_id):
    """delete: amenity object"""
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
    # amenity object not found
    abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_obj():
    """creates and returns an amenity object"""
    try:
        data = request.get_json()
    except BadRequest:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    # pass kwargs
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity_obj(amenity_id):
    """updates and returns an amenity object"""
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        if amenity.id == amenity_id:
            try:
                data = request.get_json()
            except BadRequest:
                abort(400, 'Not a JSON')
            for k, v in data.items():
                if k == 'id' or k == 'created_at' or k == 'updated_at':
                    continue
                setattr(amenity, k, v)
            storage.save()
            return jsonify(amenity.to_dict()), 200
    # amenity obj not found
    abort(404)
