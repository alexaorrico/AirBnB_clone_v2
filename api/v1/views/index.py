
#!/usr/bin/python3
"""API index views modules"""
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.user import Users
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_view.route('/status')
def status():
    """returns responses status in json format"""
    status = {"status": "OK"}
    return jsonify(status)
