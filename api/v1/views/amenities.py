#!/usr/bin/python3
"""First route to display a json object"""
from models.amenity import Amenity
from flask import jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities/', methods=['GET', 'POST'],
                 defaults={'amenity_id': None})
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'POST', 'DELETE', 'PUT'])
def amenity_views(amenity_id=None):
    if amenity_id is not None:
        my_amenity = storage.get(Amenity, amenity_id)
        if my_amenity is None:
            return jsonify(error='Amenity not found'), 404
        if request.method == 'GET':
            return jsonify(my_amenity.to_dict())
        if request.method == 'DELETE':
            storage.delete(my_amenity)
            storage.save()
            return {}, 200
        if request.method == 'PUT':
            update_values = request.get_json()
            if type(update_values) is not dict:
                return jsonify(error='Not a JSON'), 400
            for key, val in update_values.items():
                ls = ['id', 'created_at', 'updated_at']
                if key not in ls:
                    setattr(my_amenity, key, val)
                storage.save()
                return jsonify(my_amenity.to_dict())
    else:
        if request.method == 'GET':
            curr = storage.all(Amenity)
            amenity_list = []
            for item in curr.values():
                amenity_list.append(item.to_dict())
            return jsonify(amenity_list)
        if request.method == 'POST':
            new_object = request.get_json()
            if type(new_object) is not dict:
                return jsonify(error='Not a JSON'), 400
            if 'name' not in new_object.keys():
                return jsonify(error='Missing name'), 400
            new_amenity = Amenity(name=new_object['name'])
            storage.new(new_amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
