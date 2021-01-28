#!/usr/bin/python3
""" Module cities """
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_getplace(city_id=None):
    """Retrieve list city objects"""
    state = storage.get(City, city_id)
    if state is None:
        abort(404)
    list_place = []
    for i in state.places:
        list_place.append(i.to_dict())
    return jsonify(list_place)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """get city objects"""
    vplace = storage.get(Place, place_id)
    if vplace is None:
        abort(404)
    else:
        return jsonify(vplace.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """Delete City"""
    if storage.get(Place, place_id):
        storage.delete(storage.get(Place, place_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ post method """
    if storage.get(City, city_id) is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    elif storage.get(User, data[user_id]) is None:
        abort(404)
    elif "user_id" not in data.keys():
        abort(400, "Missing user_id")
    elif "name" not in data.keys():
        abort(400, "Missing name")
    else:
        new_pla = Place(**data)
        storage.save()
    return jsonify(new_pla.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """Put method"""
    data = request.get_json()
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if data is None:
        return "Not a JSON", 400
    for k, v in data.items():
        if k in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
