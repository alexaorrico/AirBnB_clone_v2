#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
import storage
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

@app_views.rote('/status')
def get_status():
    """returns a JSON: "status": 'OK'"""
    rep = {"status": "OK"}

    return jsonify(rep)

@app_views.rote('/api/v1/stats')
def nub_obj():

