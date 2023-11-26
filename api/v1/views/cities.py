#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify, abort
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """ tbc """
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    cities_list = []
    cities_dict = storage.all(City)
    for item in cities_dict:
        if cities_dict[item].to_dict()['state_id'] == state_id:
            cities_list.append(cities_dict[item].to_dict())
    if cities_list is not None:
        return cities_list


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_one_city(city_id):
    """ tbc """
    the_city = storage.get(City, city_id)
    if the_city is not None:
        return jsonify(the_city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_one_city(city_id):
    """ tbc """
    the_city = storage.get(City, city_id)
    if the_city is not None:
        storage.delete(the_city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """ tbc """
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    json_dict = request.json
    if 'name' not in json_dict:
        abort(400, description='Missing name')
    print(json_dict)
    new_city = City()
    setattr(new_city, 'state_id', state_id)
    for item in json_dict:
        setattr(new_city, item, json_dict[item])
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city_attribute(city_id):
    """ tbc """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    j = request.json
    for i in j:
        if j[i] != 'id' and j[i] != 'created_at' and j[i] != 'updated_at':
            setattr(the_city, i, j[i])
    storage.save()
    return jsonify(the_city.to_dict()), 200
