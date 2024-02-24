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


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
  """
  Create users route
  :Return: a newly created user object
  """
  user_json = request.get_json(silent=True)
  if user_json is None:
    abort(400, 'Not a JSON')
  if "email" not in user_json:
    abort(400, 'Missing email')
  if "password" not in user_json:
    abort(400, 'Missing password')
  
  new_user = User(**user_json)
  new_user.save()
  resp = jsonify(new_user.to_json())
  resp.status_code = 201
  
  return resp


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
  """
  Gets specific User object by ID
  :param user_id: user obj id
  :Return: user obj with specified id or error
  """
  
  fetched_obj = storage.get("User", str(user_id))
  
  if fetched_obj is None:
    abort(404)
    
  return jsonify(fetched_obj.to_json())


@app_views.route("/users", methods=["PUT"], strict_slashes=False)
def user_put(user_id):
  """
  Updates a specific User obj by ID
  :param user_id: user object ID
  :return: user object and 200 success, 400 or 404 on failure
  """
  user_json = request.get_json(silent_True)
  
  if user_json is None:
    abort(400, 'Not a Json')
  
  fetched_obj = storage.get("User", str(user_id))
  
  if fetched_obj is None:
    abort(404)
  
  for key, val in user_json.items():
    if key not in ["id", "created_at", "updated_at", "email"]:
      setattr(fetched_obj, key, val)

  fetched_obj.save()
  
  return jsonify(fetched_obj.to_json())


@app_views.route("/users", methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
  """
  Deletes User by ID
  :param user_id: user object id
  :Return: empty dict with 200 or 404 if not found
  """
  fetched_obj = storage.get("User", str(user_id))
  
  if fetched_obj is None:
    abort(404)

  storage.delete(fetched_obj)
  storage.save()
  
  return jsonify({})
