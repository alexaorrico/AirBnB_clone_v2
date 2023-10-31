#!/usr/bin/python3
<<<<<<< HEAD
"""index"""
from api.v1.views import app_views
from flask import jsonify
=======
<<<<<<< HEAD
"""index"""
=======
'''API status'''
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
<<<<<<< HEAD
=======
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
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7

# Mapping of class names to custom identifiers
class_name_map = {
    "users": "User",
    "places": "Place",
    "states": "State",
    "cities": "City",
    "amenities": "Amenity",
    "reviews": "Review"
}

@app_views.route('/status', methods=['GET'])
def status():
    '''Route to return status "OK"'''
    return jsonify({'status': 'OK'})

<<<<<<< HEAD
@app_views.route('/stats', methods=['GET'])
def count():
    '''Retrieves the number of objects by type'''
    object_count = {}
    for endpoint, class_name in class_name_map.items():
        object_count[endpoint] = storage.count(class_name)
    return jsonify(object_count)
=======
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
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7
