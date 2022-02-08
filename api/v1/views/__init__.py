#!/usr/bin/python3
"""Module for handling Blueprint app_views"""
from flask import Blueprint, make_response, abort, request


def retrieve_models(parent_obj, parent_obj_id, p_g):
    """[GET] - retrieves models of the given id and type"""
    parent = storage.get(parent_obj, parent_obj_id)
    if not parent:
        return make_response(jsonify({"error": "Not found"}), 404)

    return jsonify([v.to_dict() for v in getattr(parent, p_g)])


def retrieve_model(obj, id):
    """[GET] - Retrieves a model of specified type and id"""
    obj = storage.get(obj, id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(obj.to_dict())


def del_model(obj, id):
    """[DELETE] - deletes a model"""
    obj = storage.get(obj, id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)

    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


def create_model(obj, parent_obj, parent_obj_id, needed_data):
    """[POST] - creates a model"""
    from models.engine.db_storage import classes
    if parent_obj:
        parent = storage.get(parent_obj, parent_obj_id)
        if not parent:
            return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')

    for datum in needed_data:
        if datum not in data:
            msg = "Missing " + datum
            abort(400, msg)

    if "user_id" in needed_data:
        if not storage.get('User', data.get('user_id')):
            return make_response(jsonify({"error": "Not Found"}), 404)

    if parent_obj:
        data[parent_obj.lower() + '_id'] = parent_obj_id
    obj = classes[obj](**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


def update_model(obj, obj_id, auto_data):
    """[PUT] - updates a model"""
    obj = storage.get(obj, obj_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)

    received_data = request.get_json(force=True, silent=True)
    if not received_data:
        abort(400, 'Not a JSON')

    for k, val in received_data.items():
        if k not in auto_data:
            setattr(obj, k, val)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
