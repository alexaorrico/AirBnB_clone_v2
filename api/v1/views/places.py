#!/usr/bin/python3
"""index file"""

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


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    """city"""
    if storage.get('City', city_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('City', city_id).to_dict())


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_places():
    """places"""
    places_dict = []
    if storage.get('Place', place_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('Place', place_id).to_dict())


@app_views.route("/places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_places(place_id=None):
    """state"""
    willy = storage.get('Place', place_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'],
                 strict_slashes=False)
def post_city(city_id=None):
    """state"""
    try:
        willy = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if willy is None:
        abort(400, 'Not a JSON')
    elif "user_id" not in willy.keys():
        abort(400, 'Missing user_id')
    else:
        new_place = Place(name=willy['name'])
        new_state.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=['PUT'],
                 strict_slashes=False)
def put_state(place_id=None):
    """put/update state"""
    """ Request dict """
    state_store = storage.get(Place, place_id)
    try:
        dict_w = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if state_id is None:
        abort(404)
    if dict_w is None:
        abort(400, 'Not a JSON')
    for key, val in dict_w.items():
        if key == 'id' or key == 'city_id' or key == 'created_at' or\
           key == 'updated_at':
            pass
        else:
            if state_store is not None:
                setattr(state_store, key, val)
                state_store.save()
                return jsonify(state_store.to_dict()), 200
    abort(404)
