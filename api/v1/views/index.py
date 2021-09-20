#!/usr/bin/python3
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
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
    """status"""
    dict = {}
    for cls, value in classes.items():
        tot = storage.count(value)
        dict[cls] = tot
    return jsonify(dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
