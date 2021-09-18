#!/usr/bin/python3
'''index route for flask app'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """return the status"""
    return jsonify({"status": "OK"}), 200

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def count_stats():
    """return the stats""" 
    

    counts = {
	"amenities": storage.count(Amenity), 
 	"cities": storage.count(City), 
  	"places": storage.count(Place), 
  	"reviews": storage.count(Review), 
  	"states": storage.count(State), 
  	"users": storage.count(User)
    }

    return jsonify(counts), 200
