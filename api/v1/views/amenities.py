#!/usr/bin/python3
""" Handle RESTful actions for Amenity objects """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity_objects():
    """ Retrieve all Amenity objects """
    amenity_objs = [a.to_dict() for a in storage.all(Amenity)]
    return jsonify(amenity_objs)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_object(amenity_id):
    """ Retrieve a single amenity object matching the given id """
    try:
        amenity_obj = storage.get(Amenity, amenity_id).to_dict()
        return jsonify(amenity_obj)
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_object(state_id):
    """ Delete an Amenity object """
    try:
        amenity_obj = storage.get(Amenity, amenity_id)
        storage.delete(amenity_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    except:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity_object():
    """ Create an Amenity object """
    if not request.get_json():
        abort(400, description="Not a JSON")
    elif 'name' not in request.get_json():
        abort(400, description="Missing name")
    else:
        content = request.get_json()
        amenity = Amenity()
        amenity.name = content['name']
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_object(amenity_id):
    """ Update the attributes of an Amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    content = request.get_json()
    nope = ['id', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in nope:
            setattr(amenity_obj, key, value)
    storage.save()
    return make_response(jsonify(amenity_obj.to_dict()), 200)
