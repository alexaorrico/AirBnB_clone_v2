#!/usr/bin/python3
""" User view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=[
                 'GET', 'PUT', 'DELETE'])
def all_users(user_id=None):
    """ retrieves all users """

    user_list = storage.all("User").values()

    if user_id:
        try:
            user = storage.all("User").pop("User." + user_id)
        except KeyError:
            abort(404)

    if request.method == 'GET':
        if not user_id:
            my_users = [use.to_dict() for use in user_list]
            return (jsonify(my_users))
        else:
            return (jsonify(user.to_dict()))

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return (jsonify({}), 200)

    data = request.get_json(silent=True)
    if not data:
        return (jsonify({"error": 'Not a JSON'}), 400)

    if request.method == 'PUT':
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(user, k, v)
        user.save()
        return (jsonify(user.to_dict()), 200)

    if request.method == 'POST':
        for x in ["email", "password"]:
            if x not in data.keys():
                return (jsonify({"error": "Missing {}".format(x)}), 400)
        user = User(**data)
        user.save()
        return (jsonify(user.to_dict()), 201)
