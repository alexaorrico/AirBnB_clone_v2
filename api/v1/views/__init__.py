#!/usr/bin/python3
"""Init Module"""

from models.state import State

from api.v1.views.states import *
from api.v1.views.index import *

from flask import Blueprint, request, abort

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


def get_object(obj, obj_id):
    """"GET request Method"""
    query_obj = storage.get(obj, obj_id)
    if query_obj:
        return jsonify(query_obj.to_dict()), 200
    abort(404)


def delete(obj, obj_id):
    """"DELETE request Method"""
    query_obj = storage.get(obj, obj_id)
    if query_obj:
        storage.delete(query_obj)
        storage_save()
        return jsonify({}), 200
    abort(404)


def post(obj, p_obj, obj_id, data):
    """POST request Method"""
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400

    if p_obj:
        parent = storage.get(p_obj, obj_id)
        if not parent:
            abort(404)
    for key in data:
        if key not in json_data:
            return jsonify({'error': 'Missing {}'.format(key)}), 400

    if p_obj:
        aux = p_obj.__name__.lower() + "_id"
        json_data[aux] = obj_id

    _obj = (obj)(**json_data)
    _obj.save()

    return jsonify(_obj.to_dict()), 201


def put(obj, obj_id, ignore_keys):
    """PUT request Methhod"""
    json_data = request.get_json(silent=True)

    if not json_data:
        return jsonify({'error': 'Not a JSON'}), 400

    query_obj = storage.get(obj, obj_id)
    if not query_obj:
        abort(404)

    for key, value in json_data.items():
        if key not in ignore_keys:
            setattr(query_obj, key, value)
    query_obj.save()

    return jsonify(query_obj.to_dict()), 200
