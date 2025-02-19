#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


def handle_E(error=None, message="Not found", code=404):
    """Custom handler for 404 errors."""
    response = jsonify({"error": message})
    response.status_code = code
    return response


class appendRoutes():
    """append routes"""

    def __init__(self, cls, root):
        """initialize"""
        p = f'/{root}'

        @app_views.route(p, strict_slashes=False, methods=['GET', 'POST'])
        @app_views.route(f'{p}/<cls_id>', strict_slashes=False,
                         methods=['GET', 'DELETE', 'PUT'])
        def handle_API(cls_id=None):
            """
            returns a cls if cls_id provided, otherwise all clss"""
            if request.method == 'GET':
                return get_clss(cls, cls_id)
            if request.method == 'DELETE':
                return delete_cls(cls, cls_id)
            if request.method == 'POST':
                data = request.get_json(silent=True)
                if data is None:
                    return handle_E(message="Not a JSON", code=400)
                if data.get('name') is None:
                    return handle_E(message="Missing name", code=400)
                return add_cls(cls, data)
            if request.method == 'PUT':
                data = request.get_json(silent=True)
                if data is None:
                    return handle_E(message="Not a JSON", code=400)
                if data.get('name') is None:
                    return handle_E(message="Missing name", code=400)
                return update_cls(cls, cls_id, data)


def get_clss(cls, cls_id=None):
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
        storage.save()
        return jsonify({})
    else:
        return handle_E()


def add_cls(cls, data=None):
    """add new cls object"""
    if data.get('name') is None:
        return handle_E(message="Missing name", code=400)
    st = cls(name=data.get('name'))
    storage.new(st)
    tmp = cls.to_dict(st)
    tmp['status_code'] = 201
    storage.save()
    return jsonify(tmp)


def update_cls(cls, cls_id, data):
    """update cls object"""
    tmp = storage.get(cls, cls_id)
    if tmp:
        for k, v in data.items():
            if hasattr(tmp, k):
                setattr(tmp, k, v)
        storage.save()
        return jsonify(cls.to_dict(tmp))
    else:
        return handle_E()
