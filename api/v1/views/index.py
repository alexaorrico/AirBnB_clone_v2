#!/usr/bin/python3
"""Index Module
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import environ
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity
from models.user import User
app = Flask(__name__)


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/api/v1/stats')
def stats():
    """stats"""
    dict = {}
    for cls, value in classes.items():
        tot = storage.count(value)
        dict[cls] = tot
    return jsonify(dict)


if __name__ == "__main__":
    """"main function"""
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
