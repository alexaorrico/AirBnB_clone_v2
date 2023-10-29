#!/usr/bin/python3
"""api users"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route("/users", methods=["GET"])
def get_users():
    """retrieves all users object"""
    allUsers = storage.all(User).values()
    usersList = []
    for user in allUsers:
        usersList.append(user.to_dict())
    response = make_response(json.dumps(usersList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["GET"])
def get_user(id):
    """retrieves users object with id"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    response_data = user.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    """delets user with id"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users", methods=["POST"])
def create_user():
    """inserts user if its valid json amd has correct key"""
    abortMSG = "Not a JSON"
    missingEmailMSG = "Missing email"
    missingPwdMSG = "Missing password"
    if not request.get_json():
        abort(400, description=abortMSG)
    if "email" not in request.get_json():
        abort(400, description=missingEmailMSG)
    if "password" not in request.get_json():
        abort(400, description=missingPwdMSG)
    data = request.get_json()
    instObj = User(**data)
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["PUT"])
def put_user(id):
    """update a user by id"""
    abortMSG = "Not a JSON"
    user = storage.get(User, id)
    ignoreKeys = ["id", "email", "created_at", "updated_at"]
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(user, key, value)
    storage.save()
    res = user.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
