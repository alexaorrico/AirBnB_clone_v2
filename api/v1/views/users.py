#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User
from api.v1.views import custom


def handle_E(error=None, message="Not found", code=404):
    """Custom handler for 404 errors."""
    response = jsonify({"error": message})
    response.status_code = code
    return response


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/users/<cls_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def handle_API_users(cls_id=None):
    """
    returns a cls if cls_id provided, otherwise all clss"""
    cls = User
    if request.method == 'GET':
        return custom.get_cls(cls, cls_id)
    if request.method == 'DELETE':
        return custom.delete_cls(cls, cls_id)
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return custom.handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return custom.handle_E(message="Missing name", code=400)
        return custom.add_cls(cls, data)
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return custom.handle_E(message="Not a JSON", code=400)
        if data.get('name') is None:
            return custom.handle_E(message="Missing name", code=400)
        return custom.update_cls(cls, cls_id, data)


def get_cls(cls, cls_id=None):
    """
    returns a single cls if id provided, otherwise all objects in cls"""
    try:
        if cls_id:
            tmp = storage.get(cls, cls_id)
            if tmp is None:
                raise KeyError()
            tmp = cls.to_dict(tmp)
        else:
            tmp = [cls.to_dict(obj) for obj in storage.all(cls).values()]
        return jsonify(tmp)
    except KeyError:
        return handle_E()


def delete_cls(cls, cls_id=None):
    """delete cls object"""
    st = storage.get(cls, cls_id)
    if st:
        tmp = cls.delete(st)
        return jsonify({})
    else:
        return handle_E()


def add_cls(cls, data=None):
    """add new cls object"""
    if data.get('name') is None:
        return handle_E(message="Missing name", code=400)
    st = cls(data.get('name'))
    storage.new(st)
    tmp = cls.to_dict(st)
    r = jsonify(tmp)
    r.status_code = 201
    return r


def update_cls(cls, cls_id, data):
    """add new cls object"""
    st = storage.get(cls, cls_id)
    if st is None:
        return handle_E()

    data = request.get_json(silent=True)
    if data is None:
        return handle_E(message="Not a JSON", code=400)
    if data.get('name') is None:
        return handle_E(message="Missing name", code=400)
    st = cls(data.get('name'))
    storage.new(st)
    tmp = cls.to_dict(st)
    r = jsonify(tmp)
    r.status_code = 201
    return r
