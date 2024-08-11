#!/usr/bin/python3
""" A new view that handles all default api actions on the amenity  """
from api.v1.views import app_views
from flask import jsonify
from flask import abort
from flask import request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def lst_amenity():
    """ A route on the endpoint that returns an amenities list """
    all_amenities = storage.all(Amenity).values()
    amenity_obj = [obj.to_dict() for obj in all_amenities]
    return jsonify(amenity_obj), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """ A route on the endpoint that returns an amenity """
    all_amenities = storage.all(Amenity).values()
    amenity_obj = [obj.to_dict() for obj in all_amenities if
                   obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ A route that deletes an amenity based on the amenity id"""
    all_amenities = storage.all(Amenity).values()
    amenity_obj = [obj.to_dict() for obj in all_amenities if
                   obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    amenity_obj.remove(amenity_obj[0])
    for obj in all_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def post_amenity_objects():
    """ A route that allows addition of amenities to the storage"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new = Amenity(name=request.json['name'])
    storage.new(new)
    storage.save()
    amenities.append(new.to_dict())
    return jsonify(amenities[0]), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """ A route to update a specific amenity based on the amenity id"""
    all_amenities = storage.all(Amenity).values()
    amenity_obj = [obj.to_dict() for obj in all_amenities if
                   obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_obj[0]['name'] = request.json['name']
    for obj in all_amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_obj[0]), 200
