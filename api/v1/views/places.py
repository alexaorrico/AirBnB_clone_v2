#!/usr/bin/python3
""" Amenity module """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """ Retrieves a list of all Place objects linked to a City """
    places = []
    for obj in storage.all(Place).values():
        if obj.city_id == city_id:
            places.append(obj.to_dict())
    if 
    return make_response(jsonify(places), 200)


@app_views.route('/places/<place_id>', strict_slashes=False)
def one_user(place_id):
    """ Retrieves one object using its id """
    obj = storage.get(Place, place_id)
    if obj:
        return make_response(jsonify(obj.to_dict()), 200)
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """ Deletes an User obj """
    obj = storage.get(User, user_id)
    if obj:
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Creates a new User object """
    if request.is_json is True:
        data = request.get_json()
        if 'email' not in data.keys():
            abort(400, "Missing email")
        if 'password' not in data.keys():
            abort(400, "Missing password")
        obj = User(**data)
        storage.new(obj)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 201)
    abort(400, "Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates an existing User object """
    if request.is_json is True:
        data = request.get_json()
        obj = storage.get(User, user_id)
        if obj:
            for key, value in data.items():
                if key not in ['id', 'email', 'created_at', 'updated_at']:
                    setattr(obj, key, value)
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
        abort(404)
    abort(400, "Not a JSON")
