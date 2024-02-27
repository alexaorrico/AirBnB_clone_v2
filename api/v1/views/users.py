#!/usr/bin/python3
"""this is the user view for the API"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.user import User

ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""HTTP methods allowed for user"""

@app_views.route('/users', methods=ALLOWED_METHODS)
@app_views.route('/users/<user_id>', methods=ALLOWED_METHODS)
def handle_users(user_id=None):
    """handles all allowed HTTP methods to user(id)."""
    handlers = {
        'GET': get_user,
        'DELETE': del_user,
        'POST': add_user,
        'PUT': update_user,
    }
    if request.method in handlers:
        return handlers[request.method](user_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_user(user_id=None):
    """uses the GET method to retrieve a user(id)."""
    all_users = storage.all(User).values()
    if user_id:
        unique_user = [user for user in all_users if user.id == user_id]
        if unique_user:
            return jsonify(unique_user[0].to_dict())
        else:
            raise NotFound()
    else:
        all_users_dicts = [user.to_dict() for user in all_users]
        return jsonify(all_users_dicts)


def del_user(user_id=None):
    """uses the DELETE method to delete a user(id)."""
    all_users = storage.all(User).values()
    unique_user = [user for user in all_users if user.id == user_id]
    if unique_user:
        user_to_delete = unique_user[0]
        storage.delete(user_to_delete)
        storage.save()

        return jsonify({}), 200
    raise NotFound()


def add_user(user_id=None):
    """uses the POST method to add a new user"""
    try:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        if 'email' not in data:
            raise BadRequest(description='Missing email')
        if 'password' not in data:
            raise BadRequest(description='Missing password')

        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()),  201
    except Exception as e:
        # Log the exception or handle it as needed
        app.logger.error(f"Error creating user: {e}")
        raise InternalServerError(description='An error occurred \
                while creating the user')


def update_user(user_id=None):
    """uses the PUT method to update user."""
    keys_to_update = ('id', 'created_at', 'updated_at')
    all_states = storage.all(User).values()
    upd_state = [user for user in all_users if user.id == user_id]
    if upd_user:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in keys_to_update:
                setattr(upd_user[0], key, value)

        upd_user[0].save()

        return jsonify(upd_user[0].to_dict()), 200

    raise NotFound()

