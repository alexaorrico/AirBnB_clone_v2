#!/usr/bin/python3
'''Contains the index view for the API.'''
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
#from api.v1.views import app_views
from flask import jsonify

def configure_views(app_views):
    '''Configures the views'''

    @app_views.route('/status')
    def get_status():
        from api.v1.views import app_views
        '''Gets the status of the API.
        '''
        return jsonify(status='OK')


    @app_views.route('/stats')
    def get_stats():
        from api.v1.views import app_views
        '''Gets the number of objects for each type.
        '''
        objects = {
            'amenities': Amenity,
            'cities': City,
            'places': Place,
            'reviews': Review,
            'states': State,
            'users': User
        }
        for key, value in objects.items():
            objects[key] = storage.count(value)
        return jsonify(objects)
