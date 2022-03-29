#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route/status on the object app_views that returns a JSON: "status": "OK" (see example)
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from flask.json import jsonify

@app_views.route('/status', strict_slashes=False)
def return_status():
    """
    returns status
    """
    return jsonify(status="OK")
# add dict(???) for task 5