#!/usr/bin/python3
"""AirBnB clone API views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns a json object describing status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """Returns the number of each objects by type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {'amenities': Amenity, 'cities': City, 'places': Place,
               'reviews': Review, 'states': State, 'users': User}
    return jsonify({x: storage.count(classes[x]) for x in classes.keys()})
