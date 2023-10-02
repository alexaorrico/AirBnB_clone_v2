#!/usr/bin/python3
'''API Stats'''

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

@app_views.route('/stats', methods=['GET'])
def get_stats():
    '''Get the count of each object type'''
    count_dict = {}
    
    object_classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    
    for class_name in object_classes:
        count = storage.count(class_name)
        count_dict[class_name.lower() + 's'] = count
    
    return jsonify(count_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
