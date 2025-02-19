#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from models.place import Place
from api.v1.views import custom


@app_views.route('/cities/<cls_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def get_city_by_place(cls_id):
    """get/post places to respective places"""
    cls = Place
    stt = storage.get(State, cls_id)
    if stt is None:
        return custom.handle_E()
    if request.method == 'GET':
        tmp = custom.get_cls(cls)
        if tmp is None:
            return custom.handle_E()
        tmp = [obj for obj in tmp if obj["id"] == stat_id]
        return jsonify(tmp)
    if request.method == 'POST':
        if data.get('name') is None:
            return handle_E(message="Missing name", code=400)
        st = cls(data.get('name'))
        storage.new(st)
        tmp = cls.to_dict(st)
        r = jsonify(tmp)
        r.status_code = 201
        return r
    else:
        return custom.handle_E()


@app_views.route(f'places/<cls_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def handle_API_place(cls_id=None):
    """
    returns a cls if cls_id provided, otherwise all clss"""
    cls = Place
    if request.method == 'GET':
        return custom.get_cls(cls, cls_id)
    if request.method == 'DELETE':
        return custom.delete_cls(cls, cls_id)
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return custom.handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return custom.handle_E(message="Missing name", code=400)
        return custom.update_cls(cls, cls_id, data)
