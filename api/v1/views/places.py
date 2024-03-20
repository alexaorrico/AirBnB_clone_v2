#!/usr/bin/python3
""" Places API"""

from models.city import City
from models.user import User
from models.place import Place
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def placesontap(city_id=None):
    """ view Places function """
    placelist = []
    try:
        the_city = storage.get(City, city_id)
        all_places = the_city.places
        for place in all_places:
            placelist.append(place.to_dict())
        return jsonify(place_list)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id=None):
    """ get method function """
    try:
        guestplace = storage.get(Place, place_id)
        return jsonify(guestplace.to_dict())
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def place_delete(place_id=None):
    """ delete method function """
    guestplace = storage.get(Place, place_id)
    if guestplace:
        storage.delete(guestplace)
        storage.save()
        dict_empty = {}
        return make_response(jsonify(dict_empty), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def placepost(city_id=None):
    """Post method function"""
    the_city = storage.get(City, city_id)
    if not my_city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")
    all_user = storage.get(User, request.get_json().get('user_id'))
    if not all_user:
        abort(404)
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    body_obj = request.get_json()
    body_obj["city_id"] = city_id
    new_place = Place(**body_obj)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id=None):
    """Put method function"""
    guestplace = storage.get(Place, place_id)
    if not my_place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for k, v in request.get_json().items():
        if k not in ignore:
            setattr(guestplace, k, v)
    guestplace.save()
    return make_response(jsonify(guestplace.to_dict()), 200)
