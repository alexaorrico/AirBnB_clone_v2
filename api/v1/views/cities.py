#!/usr/bin/python3
"""City File"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from flask import request


@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """states"""
    if state_id is None:
        abort(404)
    cities_dict = []
    for item in storage.all('City').values():
        if storage.get('City', state_id) is state_id:
            cities_dict.append(item.to_dict())
    return jsonify(cities_dict)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_state(city_id=None):
    """state"""
    if storage.get('City', city_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('City', city_id).to_dict())


@app_views.route("/cities/<city_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_state(city_id=None):
    """state"""
    willy = storage.get('City', city_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def post_state(state_id=None):
    """state"""
    try:
        willy = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if willy is None:
        abort(400, 'Not a JSON')
    elif "name" not in willy.keys():
        abort(400, 'Missing name')
    else:
        new_city = City(name=willy['name'])
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def put_state(city_id=None):
    """put/update state"""
    """ Request dict """
    city_store = storage.get(City, city_id)
    try:
        dict_w = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if city_id is None:
        abort(404)
    if dict_w is None:
        abort(400, 'Not a JSON')
    for key, val in dict_w.items():
        if key == 'state_id' or key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            if city_store is not None:
                setattr(city_store, key, val)
                city_store.save()
                return jsonify(city_store.to_dict()), 200
    abort(404)
