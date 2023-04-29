#!/usr/bin/python3
'''
API for Amenity
'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
import models


@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def all_amenity(amenity_id=None):
    '''Returns all or an amenity object in json format'''
    json_list = []
    try:
        if amenity_id is None:
            for v in storage.all('Amenity').values():
                json_list.append(v.to_dict())
        else:
            json_list = storage.get('Amenity', amenity_id).to_dict()
        return jsonify(json_list)
    except Exception:
        abort(404)


def attrib_update(obj, **args):
    '''Helper function to update objects attributes to correct types'''
    for key, value in args.items():
        if key not in ['id', 'created_at', 'updated_at'] and hasattr(obj, key):
            if isinstance(value, str):
                value = value.replace("_", " ")
            setattr(obj, key, value)


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    '''Creates an instance of Amenity and save it to storage'''
    form = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"error": "Missing Name"}), 400
    amenity_class = models.classes['Amenity']
    new_amenity = amenity_class()
    attrib_update(new_amenity, **form)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes an amenity object'''
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    else:
        storage.delete(amenity_obj)
        storage.save()
    return jsonify({})


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    '''Updates Amenity object attribute'''
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    form = request.get_json(force=True)
    attrib_update(amenity_obj, **form)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
