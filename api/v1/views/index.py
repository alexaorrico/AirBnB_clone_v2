from models.review import Review
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.base_model import BaseModel
from . import app_views
from flask import Flask, jsonify
from models import storage


j_dict = {
    "status": "OK"
}


classes = {
    'users': User, 'places': Place,
    'states': State, 'cities': City, 'amenities': Amenity,
    'reviews': Review
}


@app_views.route('/status')
def status():
    """returns status"""
    return (jsonify(j_dict))


@app_views.route('/stats')
def stats():
    """Get stats of objects of Airbnb"""
    stats_json = {}
    for key, value in classes.items():
        stats_json[key] = storage.count(value)
    return stats_json
