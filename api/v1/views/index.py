#!/usr/bin/python3
""" tbc """
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify

@app_views.route('/status')
def index():
    """ tbc """
    return jsonify({
        "status": "OK"
        })
