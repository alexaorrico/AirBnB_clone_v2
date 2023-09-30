#!/usr/bin/python3
"""index.py to connect to API"""

from api.v1.views import app_views


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

@app_views.route('/status', strict_slashes=False)
def status():
    """method to return the status of our API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """this method returns stats of object count"""
    dic = {}
    for key, value in classes.items():
        dic[key] = storage.count(value)
    return jsonify(dic)
