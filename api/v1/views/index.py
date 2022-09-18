#!/usr/bin/python3
"""script that starts a Flask web application"""
from os import getenv
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route('/status', methods=['GET'])
def status():
    """status view"""
    return jsonify({
                    "status": "OK"
                    })

@app_views.route('/stats', methods=['GET'])
def stats():
    """stats view"""
    return jsonify({
        "amenities": storage.count(Amenity),

        "cities": storage.count(City),

        "places": storage.count(Place),

        "reviews": storage.count(Review),

        "states": storage.count(State),

        "users": storage.count(User)
    })

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST") or '0.0.0.0',
    port=getenv("HBNB_API_PORT") or 5000,
    threaded=True)
