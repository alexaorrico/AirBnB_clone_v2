#!/usr/bin/python3
""" Restful API for State objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models import storage


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Retrieves a list with all Amenity objects. """
    amenity_objs = storage.all(Amenity).values()
    list_dic_amenity = []
    for amenity in amenity_objs:
        list_dic_amenity.append(amenity.to_dict())
    return jsonify(list_dic_amenity)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object linked with amenity_id. """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete current amenity """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def new_amenity(amenity_id):
    """Create a new Amenity object. """
    body_dic = request.get_json()
    if not body_dic:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in body_dic:
        return jsonify({'error': 'Missing name'}), 400

    new_amenity = Amenity(**body_dic)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update a current Amenity"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            ignore_keys = ['id', 'created_at']
            if key not in ignore_keys:
                setattr(amenity_obj, key, value)
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict()), 200
    else:
        abort(404)
