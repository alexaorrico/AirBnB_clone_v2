#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ tbc """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    citys_places = the_city.places
    places_list = []
    for item in citys_places:
        places_list.append(item.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_one_place(place_id):
    """ tbc """
    the_place = storage.get(Place, place_id)
    if the_place is not None:
        return jsonify(the_place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_one_place(place_id):
    """ tbc """
    the_place = storage.get(Place, place_id)
    if the_place is not None:
        storage.delete(the_place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ tbc """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    json_dict = request.json
    if 'user_id' not in json_dict:
        abort(400, description='Missing user_id')
    the_user = storage.get(User, json_dict['user_id'])
    if the_user is None:
        abort(404)
    if 'name' not in json_dict:
        abort(400, description='Missing name')
    new_place = Place()
    setattr(new_place, 'city_id', city_id)
    for item in json_dict:
        setattr(new_place, item, json_dict[item])
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place_attribute(place_id):
    """ tbc """
    the_place = storage.get(Place, place_id)
    if the_place is None:
        abort(404)
    content = request.headers.get('Content-type')
    if content != 'application/json':
        abort(400, description='Not a JSON')
    j = request.json
    for i in j:
        if j[i] != 'id' and j[i] != 'created_at' and j[i] != 'updated_at':
            setattr(the_place, i, j[i])
    storage.save()
    return jsonify(the_place.to_dict()), 200
