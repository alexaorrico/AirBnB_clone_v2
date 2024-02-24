#!/usr/bin/python3

'''
Create a route '/status' on the object app_views.
'''
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods = ['GET'])
def api_status():

    '''
    Return JSON response for RESTFUL API health.
    '''
    response = {'status': 'OK'}

#task 4
@app_views.route('/status', methods = ['GET'])
def get_status():

    '''
    Retrieve the number of each object by type.
    '''
status ={
        'amenities': storage.count('Amenity')
        'cities': storage.count('City')
        'places': storage.count('Place')
        'reviews': storage.count('Review')
        'states': stogare.count('State')
        'users': storage.count('Users')
        }

return jsonify(status)
