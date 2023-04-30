#!/usr/bin/python3
'''Module for User RestAPI'''
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def user_list():
    '''Interested in list of all users'''
    if request.method == 'GET':
        user_list = storage.all('User')
        list_dict = [user.to_dict() for user in user_list.values()]
        return jsonify(list_dict)
    if request.method == 'POST':
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            if json_body['email'] is None:
                abort(400, 'Missing email')
            if json_body['password'] is None:
                abort(400, 'Missing password')
            user = User(**json_body)
            new_inst = storage.new(user)
            storage.save()
            return jsonify(user.to_dict()), 201
        except Exception as err:
            abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def user_detail(user_id):
    '''Interested in details of a specific user'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        try:
            json_body = request.get_json()
            if not json_body:
                abort(400, 'Not a JSON')
            for k, v in json_body.items():
                if k not in ['id', 'created_at', 'updated_at']:
                    setattr(user, k, v)
            storage.save()
            return jsonify(user.to_dict())
        except Exception as err:
            abort(404)
