#!/usr/bin/python3
""" Python script for State Routes & views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def get_users():
    """ Get methods for amenitites routes"""
    # get method
    if request.method == "GET":
        amenitites = []
        for user in storage.all("User").values():
            amenitites.append(user.to_dict())
        return jsonify(amenitites)

    # post method
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if not data.get("email"):
        return jsonify({'error': 'Missing email'}), 400

    if not data.get("password"):
        return jsonify({'error': 'Missing password'}), 400

    # create new user
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
def get_user_id(user_id):
    """ Get methods for retriving users objects by id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
        # return jsonify(user.to_dict())

    # DELETE method
    if request.method == "DELETE":
        user.delete()
        storage.save()
        return jsonify({}), 200

    # GET method
    elif request.method == "GET":
        return jsonify(user.to_dict())

    # PUT method
    elif request.method == "PUT":
        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({'error': 'Not a JSON'}), 400

        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        keys_ignored = {"id", "email", "created_at", "updated_at"}
        [setattr(user, k, v) for k, v in data.items() if k not in keys_ignored]
        user.save()
        return jsonify(user.to_dict()), 200
