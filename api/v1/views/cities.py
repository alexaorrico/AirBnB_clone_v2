#!/usr/bin/python3
"""Module for City api"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City


model = "City"
parent_model = "States"


def get_models(parent_model, parent_model_id, parent_getter):
    """GET api"""
    parent = storage.get(parent_model, parent_model_id)
    if not parent:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify([c.to_dict() for c in getattr(parent, parent_getter)])


def get_model(model, model_id):
    """GET api"""
    obj = storage.get(model, model_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(obj.to_dict())


def delete_model(model, model_id):
    """DELETE api"""
    obj = storage.get(model, model_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


def post_model(model, parent_model, parent_model_id, required_data):
    """POST api"""
    from models.engine.db_storage import classes
    if parent_model:
        parent = storage.get(parent_model, parent_model_id)
        if not parent:
            return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')

    for requirement in required_data:
        if requirement not in data:
            message = "Missing " + requirement
            abort(400, message)

    if "user_id" in required_data:
        if not storage.get("User", data.get("user_id")):
            return make_response(jsonify({"error": "Not found"}), 404)
    if parent_model:
        data[parent_model.lower() + '_id'] = parent_model_id
    obj = classes[model](**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


def put_model(model, model_id, ignore_data):
    """PUT api"""
    obj = storage.get(model, model_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ignore_data:
            setattr(obj, key, value)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
