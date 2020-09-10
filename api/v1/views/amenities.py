#!/usr/bin/python3
""" Restful API for State objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Retrieves a list with all Amenity objects. """
    amenity_objs = storage.all(Amenity).values()
    list_dic_amenity = []
    for amenity in amenity_objs:
        list_dic_city.append(city.to_dict())
    return jsonify(list_dic_city)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(amenity_id):
    """ Retrieves a Amenity object linked with amenity_id. """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        return jsonify(amenity_obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(amenity_id):
    """Delete current amenity """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a current City"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            ignore_keys = ['id', 'state_id', 'created_at']
            if key not in ignore_keys:
                setattr(city_obj, key, value)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
    else:
        abort(404)




@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def new_city(state_id):
    """Create a new City object. """
    body_dic = request.get_json()
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if not body_dic:
        return jsonify({'error': 'Not a JSON'}), 400
    if "name" not in body_dic:
        return jsonify({'error': 'Missing name'}), 400

    new_city = City(**body_dic)
    storage.save()
    return jsonify(new_city.to_dict()), 201
