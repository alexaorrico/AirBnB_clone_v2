#!/usr/bin/python3
""" Create a new view for State that handles all default RestFul API """

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import Flask, jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def Cities_Get(state_id):
    """ Retrieve all the states"""

    data = storage.all('City')
    state = storage.get("State", state_id)
    city_list = []
    if state is None:
        abort(404)
    states_id = "State.{}".format(state_id)
    for key, value in data.items():
        if value.state_id == state_id:
            city_list.append(value.to_dict())
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def City_Get(city_id):

    city = storage.get('City', city_id)

    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def Cities_Delete(city_id):
    """ Retrieve an state by id """
    data = storage.all('City')
    del_city = storage.get('City', city_id)
    if del_city is None:
        abort(404)
    storage.delete(del_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def Cities_Post(state_id):
    """ Post """
    data_req = request.get_json()

    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400
    if "name" not in data_req:
        return jsonify({"message": "Missing name"}), 400

    data_req.update({"state_id": state_id})
    new_city = City(**data_req)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def Cities_Put(city_id):
    """ Put """
    data = storage.get('City', city_id)
    data_req = request.get_json()

    if data is None:
        abort(404)
    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400

    for key, value in data_req.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200
