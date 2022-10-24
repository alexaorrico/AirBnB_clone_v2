#!/usr/bin/python3
"""
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """ display all places """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    response = []
    places = city.places
    for place in places:
        response.append(place.to_dict())
    return jsonify(response)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_by_id(place_id=None):
    """ display place by id """
    response = storage.get(Place, place_id)
    if response is None:
        abort(404)
    return jsonify(response.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id=None):
    """ delete place by id """
    if place_id is None:
        abort(404)
    else:
        trash = storage.get(Place, place_id)
        if trash is not None:
            storage.delete(trash)
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create new place to a specific city """
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    body = request.get_json()
    if body is None or type(body) is not dict:
        abort(400, 'Not a JSON')
    if 'name' not in body.keys():
        abort(400, 'Missing name')
    if 'user_id' not in body.keys():
        abort(400, 'Missing user_id')
    if storage.get(User, body['user_id']) is None:
        abort(400)
    body['city_id'] = city_id
    obj = Place(**body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """ update an existing place """
    response = storage.get(Place, place_id)
    if place_id is None or response is None:
        abort(404)
    try:
        new = request.get_json()
    except Exception:
        pass
    if new is None or type(new) is not dict:
        abort(400, 'Not a JSON')
    for key in new.keys():
        if key != 'id' and key != 'created_at' and key != 'city_id' and\
           key != 'user_id' and key != 'updated_at':
            setattr(response, key, new[key])
    response.save()
    return make_response(jsonify(response.to_dict()), 200)
