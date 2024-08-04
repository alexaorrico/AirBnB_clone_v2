#!/usr/bin/python3
"""Module that  handle API actions related to User objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users_method(user_id=None):
    """Func that Manipulate User object by user_id, or all objects if
    user_id is None
    """
    from models.user import User
    users = storage.all(User)

    # GET
    if request.method == 'GET':
        if not user_id:  # if no, user id specified, return all
            return jsonify([obj.to_dict() for obj in users.values()])

        key = 'User.' + user_id
        try:
            return jsonify(users[key].to_dict())
        except KeyError:
            abort(404)  # if User of user_id does not exist

    # DELETE
    elif request.method == 'DELETE':
        try:
            key = 'User.' + user_id
            storage.delete(users[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    # POST
    elif request.method == 'POST':
        # part tht convert JSON request to dict
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # the part that check for missing attributes
        if 'email' not in body_request:
            abort(400, 'Missing email')
        elif 'password' not in body_request:
            abort(400, 'Missing password')
        #the  instantiate, store, and return new User object
        else:
            new_user = User(**body_request)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201

    # PUT
    elif request.method == 'PUT':
        key = 'User.' + user_id
        try:
            user = users[key]

            # convert JSON request to dict
            if request.is_json:
                body_request = request.get_json()
            else:
                abort(400, 'Not a JSON')

            for key, val in body_request.items():
                if key != 'id' and key != 'email' and key != 'created_at'\
                   and key != 'updated_at':
                    setattr(user, key, val)

            storage.save()
            return jsonify(user.to_dict()), 200

        except KeyError:
            abort(404)

    else:
        abort(501)
