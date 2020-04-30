#!/usr/bin/python3
"""
Amenities file
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def jsonify_amenities_1():
    """ Function that returns a JSON """
    the_obj = storage.all(Amenity)
    my_list = []
    for obj in the_obj.values():
        my_list.append(obj.to_dict())
    return jsonify(my_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def jsonify_amenities_2(amenity_id):

    the_obj = storage.get(Amenity, amenity_id)
    if the_obj is None:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def jsonify_amenity_3(amenity_id):

    the_obj = storage.get(Amenity, amenity_id)
    if the_obj is None:
        abort(404)
    storage.delete(the_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def jsonify_amenity_4():
    json_post = request.get_json()
    if not json_post:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in json_post:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new = Amenity(**json_post)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def jsonify_amenity_5(amenity_id):
    the_obj = storage.get(Amenity, amenity_id)
    json_put = request.get_json()
    if the_obj is None:
        abort(404)
    if not json_put:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in json_put.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(the_obj, key, value)
    storage.save()
    return make_response(jsonify(the_obj.to_dict()), 200)
