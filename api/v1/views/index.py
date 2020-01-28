#!/usr/bin/python3
"""  """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def get_status():
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def get_stats():
    amenity = storage.count('Amenity')
    cities=storage.count('City')
    places=storage.count('Place')
    reviews=storage.count('Review')
    states=storage.count('State')
    users=storage.count('User')
    return jsonify({'amenities': amenity,
                    'cities': cities,
                    'places': places,
                    'reviews': reviews,
                    'states': states,
                    'users': users})
