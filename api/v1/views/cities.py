#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response

@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def city_get(state_id):
	result = []
	""" get all the city objects in a state """
	for i in storage.all("City").values():
		if i.state_id == state_id:
			result.append(i.to_dict())
	if len(result) == 0:
		abort(404)
	return jsonify(result)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_specific(city_id):
	""" get the specific object from city """
	for i in storage.all("City").values():
		if i.id == city_id:
			return i.to_dict()
	abort(404)

@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def city_specific_delete(city_id):
	""" delete the inputed object from city """
	task = [task for task in storage.all("City").values() if task.id == city_id]
	if len(task) == 0:
		abort(404)
	storage.delete(task[0])
	storage.save()
	return jsonify({}), 200

@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def city_specific_post(state_id):
	""" post the inputed object from city with state_id """
	if not request.json:
		return make_response("Not a JSON", 400)
	if not 'name' in request.json:
		return make_response("Missing name", 400)
	obj = classes["City"]
	try:
		new_item = obj()
		setattr(new_item, "state_id", state_id)
		setattr(new_item, "name", request.json["name"])
		new_item.save()
		return new_item.to_dict(), 201
	except:
		abort(404)

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_specific_put(city_id):
	""" update the specific object from city with city_id """
	instance = None
	if not request.json:
		return make_response("Not a JSON", 400)
	check = ["id", "created_at", "updated_at", "state_id"]
	for i in storage.all("City").values():
		if i.id == city_id:
			instance = i
			for key, value in request.json.items():
				if key not in check:
					setattr(i, key, value)
					i.save()
	if not instance:
		abort(404)
	return instance.to_dict(), 200