#!/usr/bin/python3

from ..views import app_views
from flask import jsonify, json, make_response, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def jsonresponse():
    return jsonify({'status': 'ok'})

@app_views.route('/stats')
def stats():
    dct1 = {}
    dct1["amenities"] = storage.count(Amenity)
    dct1["cities"] = storage.count(City)
    dct1["places"] = storage.count(Place)
    dct1["reviews"] = storage.count(Review)
    dct1["states"] = storage.count(State)
    dct1["users"] = storage.count(User)
    return jsonify(dct1)

@app_views.route("/cheese")
def get_one_cheese():
    resource = None

    if resource is None:
        abort(404, description="Resource not found")

    return jsonify(resource)