#!/usr/bin/python3
"""
Routes for handling User objs and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
  """
  Retrives all User objects
  :Return: json of all users
  """
  user_list = []
  user_obj = storage.all("User")
  for obj in user_obj.values():
    user_list.append(obj.to_json())
  
  return jsonify(user_list)
