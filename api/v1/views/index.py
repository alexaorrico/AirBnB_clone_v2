#!/usr/bin/python3
"""
View routes
"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    d = {"status": "OK"}
    return d


@app_views.route('/stats', strict_slashes=False)
def show():
    """
    Display Class in Json format
    """
    return jsonify({
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
        })
