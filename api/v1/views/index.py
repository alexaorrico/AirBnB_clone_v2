#!/usr/bin/python3
"""Index module"""
from api.v1.views import app_views
import json
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def index():
    """index page"""
    return json.dumps({"status": "OK"}, indent=4)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Count the number of instances for every classes"""
    return json.dumps({
        'amenities': storage.count(Amenity), 'cities': storage.count(City),
        'places': storage.count(Place), 'reviews': storage.count(Review),
        'states': storage.count(State), 'users': storage.count(User)},
                      indent=4)
