#!/usr/bin/python3
"""
Module for Place object
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """ Retrieves the list of all places of a city """
    city_obj = storage.get(City, city_id)
    if city_obj:
        places_list = []
        for place in city_obj.places:
            places_list.append(place.to_dict())
        return jsonify(places_list), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ Retrieves the dict of a Place object """
    try:
        place_dic = storage.get(Place, place_id).to_dict()
        return jsonify(place_dic)
    except:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Delete a Place object """
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Create a new Place object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    data = request.get_json()
    user_id = data['user_id']
    city_obj = storage.get(City, city_id)
    user_obj = storage.get(User, user_id)
    if city_obj and user_id:
        data['city_id'] = city_id
        new_place = Place(**data)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ Update a Place object """
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    try:
        place_obj = storage.get(Place, place_id)
        data = request.get_json()

        for key, value in data.items():
            if key != 'updated_at' or key != 'created_at':
                if key != 'id' or key != 'city_id' or key != 'user_id':
                    setattr(place_obj, key, value)

        storage.save()
        return jsonify(place_obj.to_dict()), 200
    except:
        abort(404)
