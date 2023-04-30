#!/usr/bin/python3
"""View to handle API actions related to User objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users_method(user_id=None):
    """Manipulate User object by user_id, or all objects if
    user_id is None
    """
    from models.user import User
    users = storage.all(User)

    # GET REQUESTS
    if request.method == 'GET':
        if not user_id:  # if no, user id specified, return all
            return jsonify([obj.to_dict() for obj in users.values()])

        key = 'User.' + user_id
        try:  # if obj exists in dictionary, convert from obj -> dict -> json
            return jsonify(users[key].to_dict())
        except KeyError:
            abort(404)  # if User of user_id does not exist

    # DELETE REQUESTS
    elif request.method == 'DELETE':
        try:
            key = 'User.' + user_id
            storage.delete(users[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    # POST REQUESTS
    elif request.method == 'POST':
        # convert JSON request to dict
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # check for missing attributes
        if 'email' not in body_request:
            abort(400, 'Missing email')
        elif 'password' not in body_request:
            abort(400, 'Missing password')
        # instantiate, store, and return new User object
        else:
            new_user = User(**body_request)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201

    # PUT REQUESTS
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

    # UNSUPPORTED REQUESTS
    else:
        abort(501)
