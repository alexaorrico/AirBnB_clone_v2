#!/usr/bin/python3
""" New view for Place that handles all default RESTful API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import json
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places(city_id):
    """returns State object or collection or also
    creates a new State object"""
    if request.method == 'GET':
        places = []
        city = storage.get(City, city_id)
        if city:
            for place in city.places:
                places.append(place.to_dict())
            return jsonify(places)
        else:
            abort(404)
    else:
        name = "name"
        user = "user_id"
        json_data = request.get_json(silent=True)
        city = storage.get(City, city_id)
        if city:
            if json_data is None:
                abort(400, "Not a JSON")
            if user not in json_data.keys():
                abort(400, "Missing user_id")
            user_place = storage.get(User, json_data[user])
            if user_place is None:
                abort(404)
            if name not in json_data.keys():
                abort(404, "Missing name")
            new_obj = Place(**json_data)
            new_obj.city_id = city.id
            storage.new(new_obj)
            storage.save()
            new_obj_dict = new_obj.to_dict()
            return make_response(jsonify(new_obj_dict), 201)
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def placeid(place_id):
    """Retrieves/deletes or updates a single
    object if present or rase 404"""
    if request.method == 'GET':
        obj = storage.get(Place, place_id)
        if obj is None:
            abort(404)
        obj_dict = obj.to_dict()
        return jsonify(obj_dict)
    elif request.method == 'PUT':
        obj = storage.get(Place, place_id)
        if obj is None:
            abort(404)
        json_data = request.get_json(silent=True)
        if json_data is None:
            abort(400, "Not a JSON")
        for key, val in json_data.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(obj, key, val)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        obj = storage.get(Place, place_id)
        if obj is None:
            abort(404)
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
