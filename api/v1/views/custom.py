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
    storage.save()
    response = jsonify(tmp)
    response.status_code = 201
    return response


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
