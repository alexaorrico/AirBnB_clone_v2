#!/usr/bin/python3
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenity_list():
    '''Interested in list of all amenities'''
    if request.method == 'GET':
        amenity_list = storage.all('Amenity')
        list_dict = [amenity.to_dict() for amenity in amenity_list.values()]
        return jsonify(list_dict)
    if request.method == 'POST':
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            if not 'name' in json_body:
                abort(400, 'Missing name')
            amenity = Amenity(**json_body)
            new_inst = storage.new(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
        except Exception as err:
            abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def amenity_detail(amenity_id):
    '''Interested in details of a specific amenity'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            for k, v in json_body.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, k, v)
            storage.save()
            return jsonify(amenity.to_dict())
        except Exception as err:
            abort(404)
