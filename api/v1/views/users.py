#!/usr/bin/python3
'''Users Routes'''
<<<<<<< HEAD
from flask import make_response, abort, request
=======
from flask import abort, request, jsonify
>>>>>>> eac090383e57976bf63e826af8101a492d5e60c4
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', defaults={'user_id': None}, methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def retrieve_user(user_id):
    """Gets all user or a single user"""
    if not user_id:
        data = [user.to_dict() for user in storage.all(User).values()]
    else:
        data = storage.get(User, user_id)
        if not data:
            abort(404)
        data = data.to_dict()
    return jsonify(data)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a user"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if not data.get('email'):
        abort(400, 'Missing email')
    if not data.get('password'):
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    ignored = ['id', 'email', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignored:
            if k in user.__dict__:
                setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict())
