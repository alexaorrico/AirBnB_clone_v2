#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import custom


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def get_city_by_state(state_id):
    """get/post cities to respective states"""
    stt = storage.get(State, state_id)
    if stt is None:
        return custom.handle_E()
    if request.method == 'GET':
        tmp = storage.all(City)
        if tmp is None:
            return custom.handle_E()
        tmp = [obj for obj in tmp if obj["id"] == stat_id]
        return jsonify(tmp)
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return handle_E(message="Missing name", code=400)
        st = City(data.get('name'))
        storage.new(st)
        tmp = City.to_dict(st)
        r = jsonify(tmp)
        r.status_code = 201
        return r
    else:
        return custom.handle_E()


@app_views.route('cities/<cls_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def handle_API_state(cls_id=None):
    """
    returns a cls if cls_id provided, otherwise all clss"""
    cls = City
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
