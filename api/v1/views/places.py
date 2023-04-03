#!/usr/bin/python3
""" handles all default RestFul API """


from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.city import City
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=["GET"],
                 strict_slashes=False)
def place_view(city_id):
    """ return a jsonified place objects """
    get_id = storage.get(City, city_id)
    if get_id is None:
        abort(404)
    place_dict = storage.all(Place)
    place_list = []
    for value in place_dict.values():
        if value.city_id == city_id:
            place_list.append(value.to_dict())
    return (jsonify(place_list))


@app_views.route('/places/<place_id>', methods=["GET"], strict_slashes=False)
def places_id_view(place_id):
    """ returns a jsonified place obj by place_id """
    get_id = storage.get(Place, place_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/places/<place_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ delete place obj by place_id """
    get_id = storage.get(Place, place_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """ creating a place object """
    get_id = storage.get(City, city_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "user_id" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing user_id'}), 400))
    userId = storage.get(User, data_req["user_id"])
    if userId is None:
        abort(404)
    if "name" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    data_req["city_id"] = city_id
    new_place_obj = Place(**data_req)
    new_place_obj.save()
    return (jsonify(new_place_obj.to_dict()), 201)

# @app_views.route('/places_search', methods="POST"])


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ updating a place object """
    get_id = storage.get(Place, place_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for key, value in data_req.items():
        ignore_keys = ["id", "created_at", "updated_at", "city_id", "user_id"]
        if key not in ignore_keys:
            setattr(get_id, key, value)
    get_id.save()
    return (jsonify(get_id.to_dict()), 200)
