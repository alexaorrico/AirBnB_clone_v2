#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response

@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def place_get(city_id):
	result = []
	""" get all the places in a city """
	for i in storage.all("Place").values():
		if i.city_id == city_id:
			result.append(i.to_dict())
	if len(result) == 0:
		abort(404)
	return jsonify(result)

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_specific(place_id):
	""" get the specific object from place """
	for i in storage.all("Place").values():
		if i.id == place_id:
			return i.to_dict()
	abort(404)

@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def place_specific_delete(place_id):
	""" delete the inputed object from place """
	task = [task for task in storage.all("Place").values() if task.id == place_id]
	if len(task) == 0:
		abort(404)
	storage.delete(task[0])
	storage.save()
	return jsonify({}), 200

@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def place_specific_post(city_id):
	""" post the inputed object from place objects"""
	if not request.json:
		return make_response("Not a JSON", 400)
	if not 'user_id' in request.json:
		return make_response("Missing user_id", 400)
	if not 'name' in request.json:
		return make_response("Missing name", 400)
	count = None
	for C in storage.all("City").values():
		if C.id == city_id:
			count = object
	for U in storage.all("User").values():
		if U.id == request.json["user_id"]:
			count = object
	if not count:
		abort(404)
	obj = classes["Place"]
	try:
		new_item = obj()
		for key, value in request.json.items():
			setattr(new_item, key, value)
		new_item.save()
		return new_item.to_dict(), 201
	except:
		abort(404)

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def place_specific_put(place_id):
	""" update the specific object from place objects """
	instance = None
	if not request.json:
		return make_response("Not a JSON", 400)
	check = ["id", "created_at", "updated_at", "user_id","city_id"]
	for i in storage.all("Place").values():
		if i.id == place_id:
			instance = i
			for key, value in request.json.items():
				if key not in check:
					setattr(i, key, value)
					i.save()
	if not instance:
		abort(404)
	return instance.to_dict(), 200