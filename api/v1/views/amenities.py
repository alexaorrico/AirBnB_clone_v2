#!/usr/bin/python3

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    '''gets list of all amenities objects'''
    my_list = []
    for ob in storage.all(Amenity).values():
        my_list.append(ob.to_dict())
    return jsonify(my_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    '''gets specific amenity object'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    '''deletes an amenity'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    '''Creates a new amenity'''
    j_dict = request.get_json()
    if not j_dict:
        return make_response({"error": "Not a JSON"}, 400)
    if 'name' not in j_dict:
        return make_response({"error": "Missing name"}, 400)
    amenity = Amenity(**j_dict)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_Amenity(amenity_id):
    '''update amenity object'''
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
