#!/usr/bin/python3

"""
a view for Place objects that handles all default RESTFul API actions

Authors: Khotso Selading and Londeka Dlamini
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def places(city_id):
    """retrieves of a list of all place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([obj.to_dict() for obj in city.places])


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """retrieves specific place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place(place_id):
    """deletes specific place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """adds new place object to filestorage/database"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if json_body.get('user_id') is None:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, json_body.get('user_id')) is None:
        abort(404)
    if json_body.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    json_body['city_id'] = city_id
    place = Place(**json_body)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def put_place(place_id):
    """adds new place object to filestorage/database"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_body = request.get_json()
    if json_body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in json_body.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
