#!/usr/bin/python3
""" API REST for User """
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users')
def users_all():
    """ Route return all users """
    return jsonify(list(map(lambda x: x.to_dict(),
                            list(storage.all(User).values()))))


@app_views.route('/users/<user_id>')
def users_id(user_id):
    """ Route return users with referenced id """
    my_user = storage.get('User', user_id)
    try:
        return jsonify(my_user.to_dict())
    except:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_users_id(user_id):
    """ Route delete users with referenced id """
    my_object = storage.get('User', user_id)
    if my_object is not None:
        storage.delete(my_object)
        storage.save()
    else:
        abort(404)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_users():
    """ Route create users """
    if request.is_json:
        data = request.get_json()
        if 'email' in data:
            if 'password' in data:
                new_user = User(**data)
                new_user.save()
                return jsonify(new_user.to_dict()), 201
            else:
                return jsonify(error="Missing password"), 400
        else:
            return jsonify(error="Missing email"), 400
    else:
        return jsonify(error="Not a JSON"), 400


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_users(user_id):
    """ Route update users """
    if request.is_json:
        data = request.get_json()
        my_object = storage.get('User', user_id)
        if my_object is not None:
            for keys, values in data.items():
                if keys not in ["created_at", "updated_at", "id", "email"]:
                    setattr(my_object, keys, values)
            my_object.save()
            return jsonify(my_object.to_dict()), 200
        else:
            abort(404)
    else:
        return jsonify(error="Not a JSON"), 400
