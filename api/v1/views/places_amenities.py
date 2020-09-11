#!/usr/bin/python3
"""
Rest api for Reviews
"""
from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from models.review import Review
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def show_amenity(place_id=None):
    """ Post and create object """
    flag = 0
    lista = []
    for v in storage.all(Place).values():
        if v.id == place_id:
            for amenity in v.amenities:
                lista.append(amenity.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(lista))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def Delete_amenity(place_id=None, amenity_id=None):
    """ Post and create object """
    flag = 0
    dicti = {}
    for v in storage.all(Place).values():
        if v.id == place_id:
            for amenity in v.amenities:
                if amenity.id == amenity_id:
                    storage.delete(amenity)
                    storage.save()
                    flag = 1

    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity(place_id=None, amenity_id=None):
    """ Post and create object """
    flag = 0
    for v in storage.all(Place).values():
        if v.id == place_id:
            for amenity in v.amenities:
                if amenity.id == amenity_id:
                    var2 = amenity.to_dict()
                    return (jsonify(var2), 200)

            for aminobject in storage.all(Amenity).values():
                if aminobject.id == amenity_id:
                    flag += 1
                    v.amenities.append(aminobject)
                    storage.save()
                    var = aminobject.to_dict()
    if flag == 0:
        abort(404)
    else:
        return (jsonify(var), 201)
