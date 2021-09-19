#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get():
	result = []
	""" get all the objects from state """
	for i in storage.all("State").values():
		result.append(i.to_dict())
	return jsonify(result)

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_specific(state_id):
	""" get the specific object from state """
	for i in storage.all("State").values():
		if i.id == state_id:
			return i.to_dict()
	abort(404)

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def state_specific_delete(state_id):
	""" delete the inputed object from state """
	task = [task for task in storage.all("State").values() if task.id == state_id]
	if len(task) == 0:
		abort(404)
	storage.delete(task[0])
	storage.save()
	return jsonify({}), 200

@app_views.route("/states", methods=['POST'], strict_slashes=False)
def state_specific_post():
	""" post the inputed object from state """
	if not request.json:
		return make_response("Not a JSON", 400)
	if not 'name' in request.json:
		return make_response("Missing name", 400)
	obj = classes["State"]
	new_inst = obj(**request.json)
	new_inst.save()
	return new_inst.to_dict(), 201

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_specific_put(state_id):
	""" update the specific object from state """
	instance = None
	if not request.json:
		return make_response("Not a JSON", 400)
	check = ["id", "created_at", "updated_at"]
	for i in storage.all("State").values():
		if i.id == state_id:
			instance = i
			for key, value in request.json.items():
				if key not in check:
					setattr(i, key, value)
					i.save()
	if not instance:
		abort(404)
	return instance.to_dict(), 200