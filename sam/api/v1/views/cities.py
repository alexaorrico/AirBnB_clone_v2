#!/usr/bin/python3
""" Handles all default RESTful API action relating to cities """

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models.city import City


@app_views.route(
		'/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_cities(state_id):
	"""
	Get the list of cities for a given state.

	Parameters:
	- state_id (str): The ID of the state.

	Returns:
	- tuple: A tuple containing the JSON representation
	of the list of cities and the HTTP status code.
	"""
	state = storage.get(State, state_id)
	if not state:
		abort(404, description="State not found")
	cities_all = state.cities
	cities_list = []
	for city in cities_all:
		cities_list.append(city.to_dict())
	return jsonify(cities_list), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
	"""
	Get a city by its ID.

	:param city_id: The ID of the city to retrieve.
	:return: A JSON response containing the city's information.
	:rtype: Response
	"""
	city = storage.get(City, city_id)
	if not city:
		abort(404, description="City not found")
	return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
	"""
	Deletes a city from the database.

	:param city_id: The ID of the city to be deleted.
	:type city_id: int
	:return: A JSON response indicating the success of the deletion.
	:rtype: dict
	"""
	city = storage.get(City, city_id)
	if not city:
		abort(404, description="City not found")
	city.delete()
	storage.save()
	return jsonify({}), 200


@app_views.route('/cities', strict_slashes=False, methods=['POST'])
def post_city():
	"""
	Creates a new city.

	Parameters:
	- None

	Returns:
	- tuple: A tuple containing the JSON representation
	of the new city and the HTTP status code.
	"""
	if not request.get_json():
		abort(400, description="Not a JSON")
	if 'name' not in request.get_json():
		abort(400, description="Missing name")
	if 'state_id' not in request.get_json():
		abort(400, description="Missing state_id")
	data = request.get_json()
	state = storage.get(State, data['state_id'])
	if not state:
		abort(404, description="State not found")
	new_city = City(**data)
	storage.new(new_city)
	storage.save()
	return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_city(city_id):
	"""
	Updates a city.

	:param city_id: The ID of the city to be updated.
	:type city_id: int
	:return: A JSON response indicating the success of the update.
	:rtype: dict
	"""
	city = storage.get(City, city_id)
	if not city:
		abort(404, description="City not found")
	if 'name' not in request.get_json():
		abort(400, description="Missing name")
	data = request.get_json()
	for key, value in data.items():
		if key != "id" and key != "created_at" and key != "updated_at":
			setattr(city, key, value)
	storage.save()
	return jsonify(city.to_dict()), 200
