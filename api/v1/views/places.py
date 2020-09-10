#!/usr/bin/python3
"""comment"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, Blueprint
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """our hearts pump dust and our hairs all grey"""
    lizt = []
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            lizt.append(place.to_dict())
    return jsonify(lizt)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_a_place(place_id):
    """comment"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    ret = places.to_dict()
    return jsonify(ret)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_a_place(place_id):
    """comment"""
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_a_place(city_id):
    """create a place"""
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    key = 'name'
    if key not in req:
        abort(400, description="Missing name")
    key = 'user_id'
    if key not in req:
        abort(400, description="Missing user_id")
    key = req['user_id']
    user = storage.get(User, key)
    if user is None:
        abort(404)
    req['city_id'] = city_id
    new_place = Place(**req)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_a_place(place_id):
    """ this method updates a state """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for k, value in req.items():
        if k is not "id" and k is not "created_at" and k is not "updated_at"\
           and k is not "user_id" and k is not "city_id":
            setattr(place, k, value)
    place.save()
    return jsonify(place.to_dict()), 200
