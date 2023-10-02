#!/usr/bin/python3
'''API Stats'''

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/stats', methods=['GET'])
def get_stats():
    '''Get the count of each object type'''
    count_dict = {}
    
    # Define a list of object classes
    object_classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    
    # Calculate the count for each object class
    for class_name in object_classes:
        count = storage.count(class_name)
        count_dict[class_name.lower() + 's'] = count
    
    return jsonify(count_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
