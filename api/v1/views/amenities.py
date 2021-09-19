#!/usr/bin/python3
""" return dict repersantation of object """
from models import storage
from models.engine.db_storage import classes
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get():
	result = []
	""" get all the amenity """
	for i in storage.all("Amenity").values():
		result.append(i.to_dict())
	return jsonify(result)

@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def amenity_specific(amenity_id):
	""" get the specific object from amenity """
	for i in storage.all("Amenity").values():
		if i.id == amenity_id:
			return i.to_dict()
	abort(404)

@app_views.route("/amenities/<amenity_id>", methods=['DELETE'], strict_slashes=False)
def amenity_specific_delete(amenity_id):
	""" delete the inputed object from amenity """
	task = [task for task in storage.all("Amenity").values() if task.id == amenity_id]
	if len(task) == 0:
		abort(404)
	storage.delete(task[0])
	storage.save()
	return jsonify({}), 200

@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def amenity_specific_post():
	""" post the inputed object from amenity"""
	if not request.json:
		return make_response("Not a JSON", 400)
	if not 'name' in request.json:
		return make_response("Missing name", 400)
	obj = classes["Amenity"]
	try:
		new_item = obj()
		setattr(new_item, "name", request.json["name"])
		new_item.save()
		return new_item.to_dict(), 201
	except:
		abort(404)

@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def amenity_specific_put(amenity_id):
	""" update the specific object from amenity """
	instance = None
	if not request.json:
		return make_response("Not a JSON", 400)
	check = ["id", "created_at", "updated_at"]
	for i in storage.all("Amenity").values():
		if i.id == amenity_id:
			instance = i
			for key, value in request.json.items():
				if key not in check:
					setattr(i, key, value)
					i.save()
	if not instance:
		abort(404)
	return instance.to_dict(), 200