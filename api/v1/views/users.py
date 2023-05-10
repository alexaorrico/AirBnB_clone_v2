from api.v1.views import app_views
from flask import jsonify, abort, make_response,request
from flasgger.utils import swag_from
from models import storage
from models.user import User

@app_views('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/users/users.yml')
def all_users():
    users = storage.all(User).values
    users_list = []
    
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_users(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/create_user.yml', methods=['POST'])
def create_user():
    request_data = request.get_json
    if not request_data:
        abort(400, description='Not a JSON')

    if 'email' not in request_data:
        abort(400, description='Missing email')
    if 'password' not in request_data:
        abort(400, description='Missing password')

    user = User(**request_data)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/update_user.yml', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    request_data = request.get_json
    if not request_data:
        abort(400, description='Not a JSON')

    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user:
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
