#!/usr/bin/python3

from flask import Flask
from flask.json import jsonify, request
from flask.wrappers import Request
from werkzeug.exceptions import abort
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET', 'POST'])
def states(state_id):
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
        

@app_views.route('/api/v1/cities/<city_id>/cities', methods=['GET', 'DELETE'])
def cities(city_id):
    city_obj = storage.get('City',city_id)
    if city_obj is None:
        abort(404)
        
    if request.method == 'GET':
        return jsonify(city_obj.to_json())
    
    if request.method == 'DELETE':
        city_obj.delete()
        del city_obj
        return jsonify({}), 200