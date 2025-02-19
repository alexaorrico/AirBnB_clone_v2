#!/usr/bin/python3
"""Config endpoint for REST resource states"""

from flask import Flask, abort, jsonify, make_response
from flask import request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_states(state_id=None):
    """Return all cities"""
    if state_id is not None:
        my_state_obj = storage.get(State, state_id)
        if my_state_obj is None:
            abort(404)
        else:
            cities = storage.all(City).values()
            lista = []
            for city in cities:
                if city.state_id == my_state_obj.id:
                    my_city_obj = storage.get(City, city.id)
                    lista.append(my_city_obj.to_dict())
            return jsonify(lista)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_id_(city_id=None):
    """Return city id"""
    if city_id is not None:
        my_city_obj = storage.get(City, city_id)
        if my_city_obj is None:
            abort(404)
        else:
            return jsonify(my_city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id=None):
    """DELETE city"""
    if city_id is not None:
        my_city_obj = storage.get(City, city_id)
        if my_city_obj is None:
            abort(404)
        else:
            storage.delete(my_city_obj)
            return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_post(state_id=None):
    """POST city"""
    if state_id is not None:
        my_state_obj_ = storage.get(State, state_id)
        if my_state_obj_ is None:
            abort(404)
        else:
            my_json = request.get_json(silent=True)
            if my_json is not None:
                if "name" in my_json:
                    name = my_json["name"]
                    new_city = City(name=name, state_id=state_id)
                    new_city.save()
                    return make_response(jsonify(new_city.to_dict()), 201)
                else:
                    abort(400, "Missing name")
            else:
                abort(400, "Not a JSON")


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_obj(city_id=None):
    """PUT city"""
    if city_id is not None:
        my_city_obj = storage.get(City, city_id)
        if my_city_obj is None:
            abort(404)
        else:
            update_ = request.get_json(silent=True)
            if update_ is not None:
                for key, value in update_.items():
                    setattr(my_city_obj, key, value)
                    my_city_obj.save()
                return make_response(jsonify(my_city_obj.to_dict()), 200)
            else:
                abort(400, "Not a JSON")
