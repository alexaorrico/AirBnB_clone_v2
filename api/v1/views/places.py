#!/usr/bin/python3
""" tbc """
import json
from flask import Flask, request, jsonify, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_all_places(city_id):
    """ tbc """
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    place_list = []
    place_dict = storage.all(Place)
    for item in place_dict:
        if place_dict[item].to_dict()['city_id'] == city_id:
            print(item)
            place_list.append(place_dict[item].to_dict())
    return place_list
