#!/usr/bin/python3
"""blueprint for the users"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from markupsafe import escape
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/users/<user_id>', strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """this is the view for the /api/v1/users/[SLUG]
        endpoint"""
    res = storage.get(User, escape(user_id))
    if not res:
        abort(404)
    res = res.to_dict()
    return jsonify(res)


@app_views.route('/users', strict_slashes=False, methods=["GET"])
def get_users():
    """this is the view for the /api/v1/users
        endpoint"""
    res = [x.to_dict() for x in storage.all(User).values()]
    return jsonify(res)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """this is the view for the /api/v1/users/[SLUG]
        endpoint"""
    res = storage.get(User, escape(user_id))
    if not res:
        abort(404)
    storage.delete(res)
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=["POST"])
def post_user():
    """this is the view for the /api/v1/states
        endpoint"""
    try:
        body = request.get_json()
        if 'email' not in body.keys():
            return make_response(jsonify("Missing email"), 400)
        if 'password' not in body.keys():
            return make_response(jsonify("Missing password"), 400)
        new_user = User(**body)
        storage.new(new_user)
        storage.save()
        return make_response(jsonify(new_user.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=["PUT"])
def put_user(user_id):
    """this is the view for the /api/v1/users/[SLUG]
        endpoint"""
    res = storage.get(User, escape(user_id))
    ignore_keys = ["id", "created_at", "updated_at"]
    if not res:
        abort(404)
    try:
        body = request.get_json()
        for key in body:
            if key not in ignore_keys:
                res.__dict__[key] = body[key]
        res.save()
        storage.save()
        return make_response(jsonify(res.to_dict()), 200)
    except Exception as e:
        return make_response(jsonify("Not a JSON"), 400)
