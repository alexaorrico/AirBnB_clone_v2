#!/usr/bin/python3

"""
Create a new view for City objects that handles
all default RestFul API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Return all objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    l = [obj.to_dict() for obj in city.places]
    return jsonify(l)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """ Retrieve an object """
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete an object """
    obj = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Create an object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    if not body.get("user_id"):
        abort(400, "Missing user_id")
    user = storage.get(User, body['user_id'])
    if not user:
        abort(404)
    if not body.get("name"):
        abort(400, "Missing name")
    body['city_id'] = city_id
    obj = Place(**body)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Update an object """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    for k, v in body.items():
        if k not in ['id', 'user_id', 'city_id',
                     'created_at', 'updated_at']:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
