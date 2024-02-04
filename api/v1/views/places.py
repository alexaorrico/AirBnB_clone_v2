#!/usr/bin/python3
"""
module for CRUD Place object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_of_city(city_id):
    """ retrieve the list places belongs to city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    json_obj = [c.to_dict() for c in city.places]
    return jsonify(json_obj)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """retrieve place using param id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """ remove place from storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ create new place """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data.get("user_id"))
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    new_data = data.copy()
    new_data["city_id"] = city_id
    obj_place = Place(**new_data)
    obj_place.save()
    return jsonify(obj_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ update place based on place_id"""
    ref_obj_place = storage.get(Place, place_id)
    if not ref_obj_place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key in data:
        if key not in ['id', 'id_user', 'city_id', 'created_at', 'updated_at']:
            # ref_obj_state.__dict__[key] = data[key]
            setattr(ref_obj_place, key, data[key])
    storage.save()
    return jsonify(ref_obj_place.to_dict()), 200
