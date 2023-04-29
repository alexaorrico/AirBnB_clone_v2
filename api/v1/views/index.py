from flask import jsonify, request
from app.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """A function that returns the status"""
    if request.method == 'GET':
        status = {"status": "OK"}
        return jsonify(status)


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """Route that returs the number of each objects"""
    if request.method == 'GET':
        response = {}
        OBJS = {
           "Amenity": "amenities",
           "City": "cities",
           "Place": "places",
           "Review": "reviews",
           "State": "states",
           "User": "users"
        }
    for k, v in OBJS.items():
        reponse[v] = storage.count(k)
    return jsonify(reponse)
