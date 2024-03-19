#!/usr/bin/python3
"""Users object module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request, current_app, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    pass

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user(user_id):
    pass

@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    pass

@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """the"""
    pass
