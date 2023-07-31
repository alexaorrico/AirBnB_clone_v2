#!/usr/bin/python3
"""View to handle all place objects"""

from models import storage
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, abort, request, make_response
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """Retrieve all places objects related to a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_list = []
    for plc in city.places:
        place_list.append(plc.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def one_place(place_id):
    """ Retrieves a place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Create new place object"""
    post_req = request.get_json()
    if not post_req:
        abort(400, "Not a JSON")
    if "user_id" not in post_req:
        abort(400, "Missing user_id")
    if "name" not in post_req:
        abort(400, "Missing name")

    user_id = post_req['user_id']

    __user = storage.get(User, user_id)
    __city = storage.get(City, city_id)
    if not __user or not __city:
        abort(404)

    new_place = Place(**post_req)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return make_response(new_place.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update a place object with the provided place id"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a  JSON")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    ignore_keys = ['id', 'created_id', 'updated_at', 'user_id', 'city_id']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(place.to_dict(), 200)
