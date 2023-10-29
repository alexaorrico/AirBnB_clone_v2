#!/usr/bin/python3
""" Handles all default RESTful API action relating to places """

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import Place
from models.city import City


@app_views.route(
		'/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_places(city_id):
	"""
	Get the list of places for a given city.
	"""
	city = storage.get(City, city_id)
	if not city:
		abort(404, description="City not found")
	places_all = city.places
	places_list = []
	for place in places_all:
		places_list.append(place.to_dict())
	return jsonify(places_list), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
	"""
	Get a place by its ID.
	"""
	place = storage.get(Place, place_id)
	if not place:
		abort(404, description="Place not found")
	return jsonify(place.to_dict()), 200


@app_views.route(
		'/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
	"""
	Deletes a place from the database.
	"""
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	place.delete()
	storage.save()
	return jsonify({}), 200


@app_views.route(
		'/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_place(city_id):
	"""
	Creates a new place.
	"""
	city = storage.get(City, city_id)
	if not city:
		abort(404, description="City not found")
	place = request.get_json()
	if not place:
		abort(400, description="Not a JSON")
	if 'user_id' not in place:
		abort(400, description="Missing user_id")
	if 'name' not in place:
		abort(400, description="Missing name")
	place.city_id = city_id
	place = Place(**place)
	place.save()
	return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id):
	"""
	Updates an existing place.
	"""
	place = storage.get(Place, place_id)
	if not place:
		abort(404)
	place = request.get_json()
	if not place:
		abort(400, description="Not a JSON")
	place = Place(**place)
	place.save()
	return jsonify(place.to_dict()),
	200
