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
def places(city_id):
    """returns State object or collection or also
    creates a new State object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        places = []
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    elif request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        json_data = request.get_json(silent=True)
        user_id = json_data.get("user_id")
        if not user_id:
            abort(400, "Missing user_id")
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        name = json_data.get("name")
        if not name:
            abort(400, "Missing name")
        json_data["city_id"] = city_id
        new_obj = Place(**json_data)
        new_obj.save()
        return make_response(jsonify(new_obj_dict.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def placeid(place_id):
    """Retrieves/deletes or updates a single
    object if present or rase 404"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(obj.to_dict())
    elif request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        json_data = request.get_json(silent=True)
        ignore_list = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, val in json_data.items():
            if key not in ignore_list:
                setattr(obj, key, val)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        if obj is None:
            abort(404)
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
