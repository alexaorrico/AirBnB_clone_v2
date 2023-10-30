#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/users/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/users_no_id.yml', methods=['GET', 'POST'])
def users_no_id(user_id=None):
    """
        users route that handles http requests with no ID given
    """

    if request.method == 'GET':
        all_users = storage.all('User')
        all_users = [obj.to_json() for obj in all_users.values()]
        return jsonify(all_users)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        User = CNC.get('User')
        new_object = User(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/users_id.yml', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id=None):
    """
        users route that handles http requests with ID given
    """
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_json())

    if request.method == 'DELETE':
        user_obj.delete()
        del user_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_obj.bm_update(req_json)
        return jsonify(user_obj.to_json()), 200
