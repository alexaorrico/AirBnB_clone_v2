#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.user import User
from models.place import Place
from models.state import State


@app_views.route('/status')
def index():
    return {'status': 'OK'}


@app_views.route('/stats')
def stats():
    return {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }
