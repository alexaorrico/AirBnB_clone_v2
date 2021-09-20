#!/usr/bin/python3

from flask import Flask, jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
from flask import abort
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app_views.route('/users', methods=['GET'])
def getAllusers():
    """"""
    users = []
    all = storage.all("User").values()
    for x in all:
        users.append(x.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def getByIduser(user_id):
    """"""
    users = storage.get("User", user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def deleteByIduser(user_id):
    """ """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({})


@app_views.route('/users/', methods=['POST'])
def create_users():
    """"""
    email = 'email'
    passwrd = 'password'
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if email not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if passwrd not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    data = request.get_json()
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
