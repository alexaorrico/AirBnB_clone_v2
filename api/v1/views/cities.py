#!/usr/bin/python3
"""
Module for City objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """ Retrieves the list of all cities of a state """
    state_obj = storage.get(State, state_id)
    if state_obj:
        cities_list = []
        for city in state_obj.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ Retrieves the dict of a City object """
    try:
        city_dic = storage.get(City, city_id).to_dict()
        return jsonify(city_dic)
    except:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Delete a City object """
    city_obj = storage.get(City, city_id)
    if city_obj is not None:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Create a new City object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    state_obj = storage.get(State, state_id)
    if state_obj:
        data = request.get_json()
        data['state_id'] = state_id
        new_city = City(**data)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Update a City object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    try:
        city_obj = storage.get(City, city_id)
        data = request.get_json()

        for key, value in data.items():
            if key != 'id' or key != 'created_at':
                if key != 'updated_at' or key != 'city_id':
                    setattr(city_obj, key, value)

        storage.save()
        return jsonify(city_obj.to_dict()), 200
    except:
        abort(404)
