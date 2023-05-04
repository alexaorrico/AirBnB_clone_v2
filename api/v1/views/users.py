#!/usr/bin/python3
'''
users handler
'''
from flask import Flask, make_response, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def all_users():
    '''
    all users GET & POST methods
    get returns all users
    post adds user object and saves it
    '''
    if request.method == 'GET':
        return jsonify([user.to_dict()
                        for user in storage.all('User').values()])
    if request.method == 'POST':

        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'email' not in request.get_json():
            abort(400, "Missing email")
        if 'password' not in request.get_json():
            abort(400, "Missing password")
        new_User = User(**request.get_json())
        new_User.save()

        return make_response(jsonify(new_User.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    '''
    GET / DELETE/ PUT method for User w/ specific ID
    if user_id passed doesnt exist, 404 error
    GET - returns specific user object
    DELETE - removes objecty
    PUT - updates object
    '''
    user = storage.get('User', user_id)

    if not user:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(user.to_dict()), 200)

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
