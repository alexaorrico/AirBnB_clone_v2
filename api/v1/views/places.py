#!/usr/bin/python3
""" Restful API for User objects. """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """ Retrieves a list with all places for specific City. """
    city = storage.get(City, city_id)
    if city:
        place_objs = storage.all(Place).values()
        list_places = []
        for place in place_objs:
            if place.city_id == city_id:
                list_places.append(place.to_dict())
        return jsonify(list_places)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def new_place(city_id):
    """ Retrieves a new created place """
    body_dic = request.get_json()
    city = storage.get(City, city_id)
    user = body_dic.get("user_id", None)
    if not city:
        abort(404)
    if not body_dic:
        return jsonify({'error': 'Not a JSON'}), 400
    if "user_id" not in body_dic:
        return jsonify({'error': 'Missing user_id'}), 400
    if not user:
        abort(404)
    if "name" not in body_dic:
        return jsonify({'error': 'Missing name'}), 400
    new_place = Place(**body_dic)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a current place"""
    place_obj = storage.get(Place, place_id)
    if place_obj:
        body_dic = request.get_json()
        if not body_dic:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in body_dic.items():
            ignore_keys = ['id', 'created_at', 'user_id', 'city_id']
            if key not in ignore_keys:
                setattr(place_obj, key, value)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete current place """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get current place """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)
