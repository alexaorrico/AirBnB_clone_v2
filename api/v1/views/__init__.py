#!/usr/bin/python3
''' Creating Flask App route'''


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def app_viewsRoute():
    '''doing json things for status'''
    jStatus = {'status': 'OK'}
    return jsonify(jStatus)


@app_views.route('/stats')
def stats():
    ''' returns json of object counts'''
    return jsonify(amenities=storage.count(Amenity),
                   cities=storage.count(City),
                   places=storage.count(Place),
                   reviews=storage.count(Review),
                   states=storage.count(State),
                   users=storage.count(User))
