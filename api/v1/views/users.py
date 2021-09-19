#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response

@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get():
	result = []
	""" get all the user """
	for i in storage.all("User").values():
		result.append(i.to_dict())
	return jsonify(result)

@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_specific(user_id):
	""" get the specific object from user """
	for i in storage.all("User").values():
		if i.id == user_id:
			return i.to_dict()
	abort(404)

@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def user_specific_delete(user_id):
	""" delete the inputed object from user """
	task = [task for task in storage.all("User").values() if task.id == user_id]
	if len(task) == 0:
		abort(404)
	storage.delete(task[0])
	storage.save()
	return jsonify({}), 200

@app_views.route("/users", methods=['POST'], strict_slashes=False)
def user_specific_post():
	""" post the inputed object from user"""
	if not request.json:
		return make_response("Not a JSON", 400)
	if not 'email' in request.json:
		return make_response("Missing email", 400)
	if not 'password' in request.json:
		return make_response("Missing password", 400)
	obj = classes["User"]
	try:
		new_item = obj()
		for key, value in request.json.items():
			setattr(new_item, key, value)
		new_item.save()
		return new_item.to_dict(), 201
	except:
		abort(404)

@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_specific_put(user_id):
	""" update the specific object from user """
	instance = None
	if not request.json:
		return make_response("Not a JSON", 400)
	check = ["id", "created_at", "updated_at", "email"]
	for i in storage.all("User").values():
		if i.id == user_id:
			instance = i
			for key, value in request.json.items():
				if key not in check:
					setattr(i, key, value)
					i.save()
	if not instance:
		abort(404)
	return instance.to_dict(), 200