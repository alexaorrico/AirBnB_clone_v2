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


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """states"""
    states_dict = []
    for item in storage.all('Amenity').values():
        amenities_dict.append(item.to_dict())
    return jsonify(amenities_dict)


@app_views.route("amenities/<amenity_id>", methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """state"""
    if storage.get('Amenity', amenity_id) is None:
        abort(404)
    else:
        return jsonify(storage.get('Amenity', amenity_id).to_dict())


@app_views.route("amenities/<amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id=None):
    """state"""
    willy = storage.get('Amenity', amenity_id)
    if willy is None:
        abort(404)
    else:
        storage.delete(willy)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def post_amenity(amenity_id=None):
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
        new_amenity = Amenity(name=willy['name'])
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route("amenities/<amenity_id>", methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id=None):
    """put/update state"""
    """ Request dict """
    amenity_store = storage.get(Amenity, amenity_id)
    try:
        dict_w = request.get_json()
    except:
        abort(400, 'Not a JSON')
    if amenity_id is None:
        abort(404)
    if dict_w is None:
        abort(400, 'Not a JSON')
    for key, val in dict_w.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            if amenity_store is not None:
                setattr(amenity_store, key, val)
                amenity_store.save()
                return jsonify(amenity_store.to_dict()), 200
    abort(404)
