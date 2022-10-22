from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    all_users = storage.all(User)
    users = []
    for user in all_users.values():
        users.append(user.to_dict())
    return jsonify(users)

@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    try:
        user = storage.get(User, user_id)
        return jsonify(user.to_dict())
    except KeyError:
        abort(404)

@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    try:
        user = storage.get(User, user_id)
        user.delete()
        storage.save()
        return jsonify({})
    except KeyError:
        abort(404)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    try:
        data = request.get_json()
        if data.get("name") is None:
            return make_response(jsonify({"error" : "Missing name"}), 400)
        user = User(**data)
        user.save()
        response = jsonify(user.to_dict())
        response.status_code = 201
        return response
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    try:
        data = request.get_json()
        user = storage.get(User, user_id)
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
    except KeyError:
        abort(404)
    except Exception:
        return make_response(jsonify({"error" : "Not a JSON"}), 400)
