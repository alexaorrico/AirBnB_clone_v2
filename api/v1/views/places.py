#!/usr/bin/python3
"""Create a new view for Place objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Gets all Place objects of City """
    all_place_list = []
    city_obj = storage.get(City, city_id)
    if city_obj:
        for value in storage.all(Place).values():
            if value.city_id == city_id:
                all_place_list.append(value.to_dict())
        return jsonify(all_place_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Gets a Place object """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place_obj = storage.get(Place, place_id)
    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a new Place object """
    json_body = request.get_json()
    city_obj = storage.get(City, city_id)
    if city_obj:
        if json_body:
            if 'user_id' not in json_body:
                return make_response(jsonify({'error': 'Missing user_id'}),
                                     400)
            elif 'name' not in json_body:
                return make_response(jsonify({'error': 'Missing name'}), 400)
            else:
                if storage.get(User, json_body['user_id']):
                    json_body["city_id"] = city_id
                    new_place = Place(**json_body)
                    new_place.save()
                    return make_response(jsonify(new_place.to_dict()), 201)
                else:
                    abort(404)
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object"""
    json_body = request.get_json()
    place_obj = storage.get(Place, place_id)
    if json_body:
        if place_obj:
            for key, value in json_body.items():
                if key not in ['id', 'user_id', 'city_id',
                               'created_at', 'updated_at']:
                    setattr(place_obj, key, value)
            place_obj.save()
            return make_response(jsonify(place_obj.to_dict()), 200)
        else:
            abort(404)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
