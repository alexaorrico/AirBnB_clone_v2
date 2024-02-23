#!/usr/bin/python3
'''
Create a route '/status' on the object app_views.
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    ''' routes to status page '''
   response =  {'status': 'OK'})
    return jsonify(response)

# task 4
@app_views.route("/stats")
def get_ stats():
    """Retrieve the number of each objects by type"""
    stats = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User'),
}
    return jsonify(stats)
