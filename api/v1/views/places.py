#!/usr/bin/python3

"""
A view responsible for Place entities, managing all standard RESTful API
operations.

Author:
Khotso Selading and Londeka Dlamini
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
    place_object = storage.get(City, city_id)

    if not place_object:
        abort(404)

    return jsonify([obj.to_dict() for obj in place_object.places])


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """retrieves specific place obj"""
    place_object = storage.get(Place, place_id)

    if not place_object:
        abort(404)

    return jsonify(place_object.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place(place_id):
    """deletes specific place object"""
    place_object = storage.get(Place, place_id)

    if not place_object:
        abort(404)

    place_object.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """adds new place object to filestorage/database"""
    place_object = storage.get(City, city_id)
    new_place_object = request.get_json()

    if not place_object:
        abort(404)
    if new_place_object is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if new_place_object.get('user_id') is None:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, new_place_object.get('user_id')) is None:
        abort(404)
    if new_place_object.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_place_object['city_id'] = city_id
    place = Place(**new_place_object)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def put_place(place_id):
    """adds new place object to filestorage/database"""
    place_object = storage.get(Place, place_id)
    new_place_object = request.get_json()

    if not place_object:
        abort(404)

    if new_place_object is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in new_place_object.items():
        if key not in {'id', 'created_at', 'updated_at'}:
            setattr(place_object, key, value)

    place_object.save()
    return make_response(jsonify(place_object.to_dict()), 200)
