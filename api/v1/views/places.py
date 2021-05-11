#!/usr/bin/python3
"""New view for Place objects that handles all"""

from api.v1.views import app_views
from models import storage
from flask import Flask, abort, jsonify, make_response
from models.place import Place
from models.city import City
from models.user import User
from flask import request
from models.state import State


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_place(city_id=None):
    """Retrieves the list of all Place objects of a City"""
    if city_id is not None:
        my_city_obj = storage.get(City, city_id)
        if my_city_obj is None:
            abort(404)
        else:
            places = storage.all(Place).values()
            lista = []
            for place in places:
                if place.city_id == my_city_obj.id:
                    my_place_obj = storage.get(Place, place.id)
                    lista.append(my_place_obj.to_dict())
            return jsonify(lista)


@app_views.route('/places/<place_id>', methods=['GET'])
def place_id_(place_id=None):
    """Return a place by its id"""
    if place_id is not None:
        my_place_obj = storage.get(Place, place_id)
        if my_place_obj is None:
            abort(404)
        else:
            return jsonify(my_place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id=None):
    """Delete place by its id"""
    if place_id is not None:
        my_place_obj = storage.get(Place, place_id)
        if my_place_obj is None:
            abort(404)
        else:
            storage.delete(my_place_obj)
            return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_post(city_id=None):
    """POST a place"""
    if city_id is not None:
        my_city_obj_ = storage.get(City, city_id)
        if my_city_obj_ is None:
            abort(404)
        else:
            my_json = request.get_json(silent=True)
            if my_json is not None:
                if "user_id" in my_json:
                    my_user_obj_ = storage.get(User, my_json['user_id'])
                    if my_user_obj_ is not None:
                        if "name" in my_json:
                            name = my_json["name"]
                            n = Place(name=name, user_id=my_json['user_id'],
                                      city_id=city_id)
                            n.save()
                            return make_response(jsonify(n.to_dict()), 201)
                        else:
                            abort(400, "Missing name")
                    else:
                        abort(404)
                else:
                    abort(400, "Missing user_id")
            else:
                abort(400, "Not a JSON")


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_obj_places(place_id=None):
    """PUT place"""
    if place_id is not None:
        my_place_obj = storage.get(Place, place_id)
        if my_place_obj is None:
            abort(404)
        else:
            update_ = request.get_json(silent=True)
            if update_ is not None:
                for key, value in update_.items():
                    setattr(my_place_obj, key, value)
                    my_place_obj.save()
                return make_response(jsonify(my_place_obj.to_dict()), 200)
            else:
                abort(400, "Not a JSON")
