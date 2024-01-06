#!/usr/bin/python3
""" Index view for the API """
from flask import jsonify
from api.v1.views import app_views
from models import storage
<<<<<<< Updated upstream
=======
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
>>>>>>> Stashed changes


@app_views.route('/status')
def get_status():
    """Gets the status of the API"""
    return jsonify(status='OK')

<<<<<<< Updated upstream

@app_views.route('/stats')
def statistics():
    """Retuens the number of objects in storage"""
    stats = storage.count()
    response_body = jsonify(stats)
    status_code = 200
    return response_body, status_code
=======
@app_views.route('/stats')
def get_stats():
    """Gets number of objects for each type"""
    objects = {
        'amenitties': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
>>>>>>> Stashed changes
