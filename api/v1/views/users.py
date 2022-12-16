#!/usr/bin/python3
""" new view for Amenities objects """
from models import storage
from api.v1.views import app_views
from models.user import User
from flask import make_response, jsonify
from flask import request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>')
def get_users(user_id=None):
    """ Retrieves the list of all State objects """
    if user_id is None:
        users_objs = [user.to_dict() for user in
                      storage.all(User).values()]
        return make_response(jsonify(users_objs), 200)
    else:
        obj = storage.get(User, user_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    obj = storage.get(User, user_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def post_user():
    data = request.get_json(silent=True, force=True)
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'email' not in data:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in data:
            return make_response(jsonify({'error': 'Missing password'}), 400)
    obj = User(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def put_amenities(user_id=None):
    if user_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        obj = storage.get(User, user_id)
        if obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            data = request.get_json(silent=True, force=True)
            if data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(obj, item, value) for item, value in data.items()
             if item != ('id', 'email', 'created_at', 'updated_at')]
            obj.save()
            return make_response(jsonify(obj.to_dict()), 200)
