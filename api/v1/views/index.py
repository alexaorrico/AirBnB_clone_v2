#!/usr/bin/python3

from ..views import app_views
from flask import jsonify, json, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def jsonresponse():
    return json.dumps({"status": "ok"}, indent=4)

@app_views.route('/stats')
def stats():
    dct1 = {}
    dct1["amenities"] = storage.count(Amenity)
    dct1["cities"] = storage.count(City)
    dct1["places"] = storage.count(Place)
    dct1["reviews"] = storage.count(Review)
    dct1["states"] = storage.count(State)
    dct1["users"] = storage.count(User)
    return json.dumps(dct1, indent=4)
