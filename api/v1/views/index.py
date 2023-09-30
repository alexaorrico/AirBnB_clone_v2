#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json

classes = {"amenities": Amenity,"cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'])
def status():
    data = {
        "status": "OK"
    }
    # response = json.dumps(data, indent=2)
    # print("type of res is ", type(response))
    # response += '\n'
    # return response
    print("type is ", type(data))
    return data

@app_views.route('/stats', methods=['GET'])
def stats():
    count_dict = {}

    for key, value in classes.items():
        count_dict[key] = storage.count(value)
    
    response = json.dumps(count_dict, indent=2)
    response += '\n'
    return response

@app_views.errorhandler(404)
def not_found_error(error):
    data = {
        "error": "Not found"
    }

    response = json.dumps(data, indent=2)
    response += '\n'
    return response
