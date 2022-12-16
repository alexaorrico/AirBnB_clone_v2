#!/usr/bin/python3
""" new view for State objects """
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from flask import Flask, make_response, jsonify
import requests
from flask import request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id=None):
    obj = storage.get(City, city_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    places_objs = [place.to_dict() for place in storage.all(Place).values()
                   if place.city_id == city_id]
    return make_response(jsonify(places_objs), 200)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    obj = storage.get(Place, place_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ Method DELETE """
    obj = storage.get(Place, place_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    data = request.get_json(silent=True, force=True)
    obj = storage.get(City, city_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        if 'user_id' not in data:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
    objs = Place(**data)
    objs.city_id = city_id
    objs.save()
    return make_response(jsonify(objs.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id=None):
    if place_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        obj = storage.get(Place, place_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            data = request.get_json(silent=True, force=True)
            if data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(obj, key, value) for key, value in data.items()
             if key != (
                'id', 'user_id', 'created_at', 'city_id',
                'updated_at', 'state_id'
                )]
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
