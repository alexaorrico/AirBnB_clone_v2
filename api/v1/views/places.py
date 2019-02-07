#!/usr/bin/python3
"""view of State object"""
from api.v1.views import app_views
from models import storage, place, city, user
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=["GET"])
def place_ret(city_id):
    """return json Place objects"""
    place_list = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=["GET"])
def place_get_by_id(place_id):
    """return json Place objects by id"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"])
def place_delete(place_id=None):
    """delete an object by id"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=["POST"])
def post_place_obj(city_id):
    """add new place object"""
    dic = {}
    if storage.get("City", city_id) is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "user_id" not in dic.keys():
        abort(400, "Missing user_id")
    if storage.get("User", dic["user_id"]) is None:
        abort(404)
    if "name" not in dic.keys():
        abort(400, "Missing name")
    new_place = place.Place()
    setattr(new_place, "city_id", city_id)
    for k, v in dic.items():
        setattr(new_place, k, v)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"])
def update_place_obj(place_id=None):
    """update new state object"""
    dic = {}
    list_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        if key not in list_key:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
