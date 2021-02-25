#!/usr/bin/python3
""" new view for Place objects """

from models.place import Place
from models.city import City
from models.user import User
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, base_model


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['GET']
)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    if request.method == 'GET':
        city_obj = storage.get(City, city_id)
        if not city_obj:
            return abort(404)
        Place_list = []
        for ob in city_obj.places:
            Place_list.append(ob.to_dict())
        return jsonify(Place_list), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_Place_id(place_id):
    """Retrieves a Place by id"""
    if request.method == 'GET':
        ob = storage.get(Place, place_id)
        if ob is not None:
            return jsonify(ob.to_dict())
        else:
            return abort(404)


@app_views.route(
    '/places/<place_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_Place_ob(place_id):
    """Delete a Place object by id"""
    if request.method == 'DELETE':
        ob = storage.get(Place, place_id)
        if ob is not None:
            storage.delete(ob)
            storage.save()
            return jsonify({}), 200
        else:
            return abort(404)


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['POST']
)
def create_Place_ob(city_id):
    """Create a Place object"""
    if request.method == 'POST':
        city_ob = storage.get(City, city_id)
        if not city_ob:
            return abort(404)
        place_req = request.get_json()
        if not place_req:
            return "Not a JSON", 400
        if "user_id" not in place_req.keys():
            return "Missing user_id", 400
        user_ob = storage.get(User, place_req["user_id"])
        if not user_ob:
            return abort(404)
        if "name" not in place_req:
            return "Missing name", 400
        else:
            ob = Place(**place_req)
            ob.city_id = city_id
            storage.new(ob)
            storage.save()
            return jsonify(ob.to_dict()), 201


@app_views.route(
    '/places/<place_id>',
    strict_slashes=False,
    methods=['PUT']
)
def update_Place_ob(place_id):
    """Update a Place object"""
    if request.method == 'PUT':
        ob = storage.get(Place, place_id)
        data = request.get_json()
        if not ob:
            return abort(404)
        if not data:
            return "Not a JSON", 400
        list_keys = [
            "id",
            "created_at",
            "updated_at",
            "user_id",
            "city_id"
        ]
        for key, val in data.items():
            if key not in list_keys:
                setattr(ob, key, val)
        storage.save()
        return jsonify(ob.to_dict()), 200
