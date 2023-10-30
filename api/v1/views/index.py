#!/usr/bin/python3
<<<<<<< HEAD
"""index"""
=======
'''API status'''
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from flask import jsonify
>>>>>>> 84f4a9ee1c4103d1f3dbe18eb210bc4996364844
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    '''Returns the API status.'''
    return jsonify(status="OK")

<<<<<<< HEAD
@app_views.route('/status', methods=['GET'])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''retrieves the number of each objects by type'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
=======
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    '''Returns the count of each type of object.'''
    classes = {
        "states": State,
        "users": User,
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review
    }
    stats = {key: storage.count(value) for key, value in classes.items()}
    return jsonify(stats)
>>>>>>> 84f4a9ee1c4103d1f3dbe18eb210bc4996364844
