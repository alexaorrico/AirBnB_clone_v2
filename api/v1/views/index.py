#!/usr/bin/python3
"""
routes
"""
from api.v1.views import app_views
# api/v1/views/index.py
from flask import jsonify, Blueprint
from models import storage
import models
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.review import Review
from models.city import City

app_views = Blueprint('app_views', __name__)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each object by type"""
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    stats = {cls.lower(): storage.count(eval(cls)) for cls in classes}
    return jsonify(stats)
