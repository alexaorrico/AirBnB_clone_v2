#!/usr/bin/python3
""" retruns json response status of API """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


app = Flask(__name__)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def get_state(state_id):
    

to_dict()
