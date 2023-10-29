#!/usr/bin/python3
""" Returns Amenity object with status -> (code 200) """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users_method(user_id=None):
    """ Retrieves a Amenity """
    users = storage.all(User)

    # GET ALL REQUESTS
    if request.method == 'GET':
        if not user_id:
            return jsonify([obj.to_dict() for obj in users.values()])
        key = 'User.' + user_id
        try:
            return jsonify(users[key].to_dict())
        except KeyError:
            abort(404)

    # DELETE ALL REQUESTS
    elif request.method == 'DELETE':
        try:
            key = 'User.' + user_id
            storage.delete(users[key])
            storage.save()
            return jsonify({}), 200
        except:
            abort(404)

    # POST ALL REQUESTS
    elif request.method == 'POST':
        if request.is_json:
            body_request = request.get_json()
        else:
            abort(400, 'Not a JSON')

        # checking for missing attributes
        if 'email' not in body_request:
            abort(400, 'Missing email')
        elif 'password' not in body_request:
            abort(400, 'Missing password')
        else:
            new_user = User(**body_request)
            storage.new(new_user)
            storage.save()
            return jsonify(new_user.to_dict()), 201

    # PUT ALL REQUESTS
    elif request.method == 'PUT':
        key = 'User.' + user_id
        try:
            user = users[key]
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
