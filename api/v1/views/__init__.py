#!/usr/bin/python3
"""Module for Blueprint app_views"""
from flask import Blueprint, abort, make_response


def get_models(parent_model, parent_model_id, parent_getter):
    """GET /model api route"""
    parent = storage.get(parent_model, parent_model_id)
    if not parent:
        return make_response(jsonify({"error": "Not found"}), 404)

    return jsonify([c.to_dict() for c in getattr(parent, parent_getter)])


def get_model(model, model_id):
    """GET /model api route"""
    obj = storage.get(model, model_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)

    return jsonify(obj.to_dict())


def delete_model(model, model_id):
    """DELETE /model api route"""
    obj = storage.get(model, model_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)

    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


def post_model(model, parent_model, parent_model_id, required_data):
    """POST /model api route"""
    from models.engine.db_storage import classes
    if parent_model:
        parent = storage.get(parent_model, parent_model_id)
        if not parent:
            return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        # return make_response(jsonify({"error": "Not a JSON"}), 400)
        abort(400, 'Not a JSON')

    for requirement in required_data:
        if requirement not in data:
            message = "Missing " + requirement
            # return make_response(jsonify({"error": message}), 400)
            abort(400, message)

    if "user_id" in required_data:  # TODO: does this work?
        if not storage.get("User", data.get("user_id")):
            return make_response(jsonify({"error": "Not found"}), 404)

    if parent_model:
        data[parent_model.lower() + '_id'] = parent_model_id
    obj = classes[model](**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


def put_model(model, model_id, ignore_data):
    """PUT /model api route"""
    obj = storage.get(model, model_id)
    if not obj:
        return make_response(jsonify({"error": "Not found"}), 404)

    data = request.get_json(force=True, silent=True)
    if not data:
        # return make_response(jsonify({"error": "Not a JSON"}), 400)
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ignore_data:
            setattr(obj, key, value)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
