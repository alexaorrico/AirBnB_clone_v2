#!/usr/bin/python3
"""module state"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenity():
    """state"""
    list_amenity = []
    for amenity_objs in storage.all('Amenity').values():
            list_amenity.append(amenity_objs.to_dict())
    return jsonify(list_amenity)


@app_views.route('/amenities/<id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_delete(id=None):
    """state delete"""
    obj_amenity = storage.get('Amenity', id)
    if obj_amenity is None:
        abort(404)
    if request.method == 'DELETE':
        obj_amenity.delete()
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        do_put = request.get_json()
        if not do_put:
            return jsonify({'error': 'Not a JSON'}), 400
        [setattr(obj_amenity, k, v) for k, v in do_put.items()
         if k not in ["id", "created_at", "updated_at"]]
    obj_amenity.save()
    return jsonify(obj_amenity.to_dict()), 200


@app_views.route('/amenities', methods=['POST'])
def amenity_post():
    """state post"""
    if request.json:
        if "name" in request.json:
            do_post = request.get_json()
            new_obj = Amenity(**do_post)
            new_obj.save()
            return jsonify(new_obj.to_dict()), 201
        else:
            return jsonify({'error': 'Missing name'}), 400
    else:
        return jsonify({'error': 'Not a JSON'}), 400
