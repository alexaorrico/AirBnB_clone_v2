#!/usr/bin/python3
"""The Index file for package views"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models import storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


models = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
        }
        
        
@app_views.route('/status', methods['GET'])
def get_status():
    """function returns server status"""
    return jsonify(status="OK")
    
    
@app_views.route('/stats')
 def get_stats():
     """function returns stats of all models"""
     stats = {}
     for name, model in models.items():
         total = storage.count(model)
         stats[name] = total
     return jsonify(stats)
