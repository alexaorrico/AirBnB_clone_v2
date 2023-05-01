#!/usr/bin/python3

'''
Index file that renders the index.html template
Routes:
    /status: Returns a JSON : "status": "OK"
    /stats: Returns a JSON with the number of objects by type
'''

from flask import Flask, render_template, jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    '''Returns a JSON : "status": "OK"'''
    return jsonify(
            {
                "status": "OK"
            })


@app_views.route('/stats', methods=['GET'])
def stats():
    '''Returns a JSON with the number of objects by type'''
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    from models.user import User

    return jsonify({'amenities': storage.count(Amenity),
                    'cities': storage.count(City),
                    'places': storage.count(Place),
                    'reviews': storage.count(Review),
                    'states': storage.count(State),
                    'users': storage.count(User)
                    })
