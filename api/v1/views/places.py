#!/usr/bin/python3
"""
places
"""
from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places_get(city_id=None):
    """ Show all places objects """
    lista = []
    flag = 0
    for v in storage.all(City).values():
        if v.id == city_id:
            for place in v.places:
                lista.append(place.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(lista))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def all_places(place_id=None):
    """ Show one place object """
    flag = 0
    for v in storage.all(Place).values():
        if v.id == place_id:
            attr = (v.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr))


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places(place_id=None):
    """ delete a place """
    if place_id is None:
        abort(404)
    dicti = {}
    flag = 0
    for v in storage.all(Place).values():
        if v.id == place_id:
            storage.delete(v)
            storage.save()
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_places(city_id=None):
    """ Create a object place """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    if 'user_id' not in request.json:
        abort(400, "Missing user_id")
    result = request.get_json()
    obj = Place()
    flag = 0
    for v in storage.all(City).values():
        if v.id == city_id:
            for user in storage.all(User).values():
                if result["user_id"] == user.id:
                    for k, values in result.items():
                        flag += 1
                        setattr(obj, k, values)
                        if flag == 1:
                            setattr(obj, "city_id", city_id)
                            flag += 1
                    storage.new(obj)
                    storage.save()
                    var = obj.to_dict()
    if flag == 0:
        abort(404)
    else:
        return (jsonify(var), 201)


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def change_places(place_id=None):
    """ change a atribute of place """
    if not request.json:
        abort(400, "Not a JSON")

    result = request.get_json()
    flag = 0
    for values in storage.all(Place).values():
        if values.id == place_id:
            for k, v in result.items():
                setattr(values, k, v)
                storage.save()
                attr = (values.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr), 200)
