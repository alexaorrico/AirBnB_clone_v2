#!/usr/bin/python3
"""
  Cities Restful api
"""

from flask import jsonify, abort, request
from models import storage
from models.city import City
from api.v1.views import app_views

@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
  """return all cities for state"""
  state = storage.get("State", state_id)
  if not state:
    abort(404)
  cities = storage.all('City').values()
  result = filter(lambda city: city.state_id == state_id, cities)
  result = map(lambda city: city.to_dict(), result)
  return jsonify(list(result))

@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
  """GET city"""
  city = storage.get('City', city_id)
  if city is None:
    abort(404)
  
  return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
  """DELETE city"""
  city = storage.get('City', city_id)
  if city is None:
    abort(404)
  
  storage.delete(city)
  storage.save()
  return jsonify({})

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def add_city(state_id):
  """POST city"""
  state = storage.get('State', state_id)
  if state is None:
    abort(404)

  data = request.get_json()
  if data is None:
      abort(400, "Not a JSON")
  if 'name' not in data:
      abort(400, "Missing name")
  city = City(**data)
  city.state_id = state_id
  city.save()
  city = city.to_dict()
  return jsonify(city), 201

@app_views.route('/cities/<city_id>', methods=['PUT'])
def edit_city(city_id):
  '''PUT city'''
  city = storage.get("City", city_id)
  if city is None:
    abort(404)
  data = request.get_json()
  if data is None:
    abort(400, "Not a JSON")
  
  for key, value in data.items():
    if key not in ["id", "created_at", "updated_at"]:
      setattr(city, key, value)
  city.save()
  return jsonify(city.to_dict()), 201