#!usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
    #for key in objects.keys():
        #objects[key] = key[0].upper()+key[1:-1]storage.count(key[0].upper()+key[1:-1])
   # return jsonify(objects)

