#!/usr/bin/python3
""" prepares data for easier viewing """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import OperationalError


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """ Returns all the user obj in json """
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users', methods=['POST'])
@app_views.route('/users/<user_id>', methods=['DELETE', 'GET', 'PUT'])
def get_put_delete_user(user_id=None):
    """ gets or deletes user from storage """
    if user_id:
        user = storage.get('User', user_id)
    else:
        user = None

    if not user and request.method != 'POST':
        abort(404)

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({})

    if request.method != 'GET':
        """ handles put and post """
        if request.mimetype != 'application/json':
            return jsonify(error="Not a JSON"), 400
        try:
            user_json = request.get_json()
        except BadRequest:
            return jsonify(error="Not a JSON"), 400

        if request.method == 'PUT':
            if user_json.get('id'):
                user_json.pop('id')
            if user_json.get('created_at'):
                user_json.pop('created_at')
            if user_json.get('updated_at'):
                user_json.pop('updated_at')
            if user_json.get('email')
                user_json.pop('email')
            for k, v in user_json.items():
                setattr(user, k, v)
                user.save()

        if request.method == 'POST':
            user = User(**user_json)
            if "email" not in user_json:
                return jsonify(error="Missing email"), 400
            if "password" not in user_json:
                return jsonify(error="Missing password"), 400
            
            return jsonify(user.to_dict()), 201

    return jsonify(user.to_dict())