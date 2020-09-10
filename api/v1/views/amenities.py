#!/usr/bin/python3
"""
Module for amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', defaults={'amenity_id': None}, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities(amenity_id):
    """ Retrieves the list of all Amenity objects """
    if amenity_id is None:
        amenities_list = []
        for value in storage.all(Amenity).values():
            amenities_list.append(value.to_dict())
        return jsonify(amenities_list)
    else:
        try:
            amenity_dic = storage.get(Amenity, amenity_id).to_dict()
            return jsonify(amenity_dic)
        except:
            abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ Create a new Amenity object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    data = request.get_json()
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Update a Amenity object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    try:
        amenity_obj = storage.get(Amenity, amenity_id)
        data = request.get_json()

        for key, value in data.items():
            if key != 'id' or key != 'created_at' or key != 'updated_at':
                setattr(amenity_obj, key, value)

        storage.save()
        return jsonify(amenity_obj.to_dict()), 200
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Delete a amenity object """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is not None:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
