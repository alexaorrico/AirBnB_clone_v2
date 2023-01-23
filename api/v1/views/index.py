#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status')
def response():
  """Status: Ok"""
  dic = {"status": "OK"}
  return jsonify(dic)

@app_views.route('/status')
def class_counter():
  """Get a dictionary from count method"""
  dic = {}
  dic["amenities"] = storage.count("Amenity")
  dic["city"] = storage.count("City")
  dic["place"] = storage.count("Place")
  dic["reviews"] = storage.count("Reviews")
  dic["states"] = storage.count("States")
  dic["users"] = storage.count("Users")
  return jsonify(dic)
