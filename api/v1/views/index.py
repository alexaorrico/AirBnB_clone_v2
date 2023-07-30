#!/usr/bin/python3
"""display status OK!"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def view_status():
    """Return the status OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def view_stats():
    """Returns every class and count number of instances"""
    from models import storage
    return jsonify({
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'user': storage.count(User)})
