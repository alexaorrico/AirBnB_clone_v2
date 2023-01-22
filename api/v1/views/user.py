from models import storage
from models.user import User
from . import app_views
from flask import jsonify, abort, request

@app_views.route("/users")
def users():
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)

@app_views.route("/users/<user_id>")
def user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route("/users/<user_id>")
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})

@app_views.route("/users", methods=["POST"])
def create_user():
    if request.content_type != "application/json":
        abort(404)
    data = request.get_json()
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    data = request.get_json()
    if "id" in data:
        data.pop("id")
    if "email" in data:
        data.pop("email")
    if "created_at" in data:
        data.pop("created_at")
    if "updated_at" in data:
        data.pop("updated_at")
    for key, value in data.items():
        user.__setattr__(key, value)
    user.save()
    return jsonify(user.to_dict())