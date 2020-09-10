#!/usr/bin/python3
""" ameniti rest api """
from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def allAmenitys(amenity_id=None):
    """ show all and one amenitie object """
    if amenity_id is None:
        lista = []
        for v in storage.all(Amenity).values():
            lista.append(v.to_dict())
        return (jsonify(lista))
    else:
        flag = 0
        for v in storage.all(Amenity).values():
            if v.id == amenity_id:
                attr = (v.to_dict())
                flag = 1
        if flag == 0:
            abort(404)
        else:
            return (jsonify(attr))


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities(amenity_id=None):
    """ delete an amenity object """
    if amenity_id is None:
        abort(404)
    dicti = {}
    flag = 0
    for v in storage.all(Amenity).values():
        if v.id == amenity_id:
            storage.delete(v)
            storage.save()
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_task_amenities():
    """ create an amenity object """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    result = request.get_json()
    obj = Amenity()
    for k, v in result.items():
        setattr(obj, k, v)
    storage.new(obj)
    storage.save()
    var = obj.to_dict()
    return (jsonify(var), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_task_amenities(amenity_id=None):
    """ change an atribute of amenity object """
    if not request.json or 'name' not in request.json:
        abort(400, "Not a JSON")
    if amenity_id is None:
        abort(404)

    result = request.get_json()
    flag = 0
    for values in storage.all(Amenity).values():
        if values.id == amenity_id:
            for k, v in result.items():
                setattr(values, k, v)
                storage.save()
                attr = (values.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(attr), 200)
