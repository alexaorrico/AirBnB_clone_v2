#!/usr/bin/python3
"""New view for Place object that handles all default RestfulApi actions"""
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_objs(city_id=None):
    """Return all Place objects in a City"""
    place_objs_city = storage.get(City, city_id)
    if place_objs_city:
        return jsonify([place.to_dict() for place in place_objs_city.places])
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_by_id(place_id=None):
    """Retrieves a place by its id"""
    place_obj = storage.get(Place, place_id)
    if place_obj:
        return jsonify(place_obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a Place object"""
    place_objs = storage.get(Place, place_id)
    if place_objs:
        storage.delete(place_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id=None):
    """Create Place object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    dict_body = request.get_json()
    city_objs = storage.get(City, city_id)
    user_info = storage.get(User, dict_body['user_id'])
    if city_objs and user_info:
        new_place = Place(**dict_body)
        new_place.city_id = city_objs.id
        storage.new(new_place)
        storage.save()
        return make_response(jsonify(new_place.to_dict()), 201)
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id=None):
    """Update Place object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    dict_body = request.get_json()
    place_obj = storage.get(Place, place_id)
    if place_obj:
        for key, value in dict_body.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
               and key != "user_id" and key != "city_id":
                setattr(place_obj, key, value)
        storage.save()
        return make_response(jsonify(place_obj.to_dict()), 200)
    else:
        return abort(404)
